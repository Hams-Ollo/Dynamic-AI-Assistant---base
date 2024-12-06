from typing import Dict, List, Optional, Any, Union
import uuid
from datetime import datetime
import logging
from pathlib import Path
import os
from dotenv import load_dotenv

from langchain_community.document_loaders import (
    TextLoader,
    UnstructuredMarkdownLoader,
    PDFMinerLoader,
    Docx2txtLoader
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
import chromadb
from chromadb.config import Settings
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

from .emoji_logger import EmojiLogger
from tqdm import tqdm

class DocumentProcessor:
    """Handles document processing, chunking, and vectorization."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize document processor with configuration."""
        self.config = config or {}
        self.logger = EmojiLogger
        
        # Load environment variables
        load_dotenv()
        
        # Set up paths
        self.base_path = Path("data/documents")
        self.documents_path = self.base_path / "metadata"
        self.vector_store_path = self.base_path / "vector_store"
        
        # Ensure directories exist
        self.documents_path.mkdir(parents=True, exist_ok=True)
        self.vector_store_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize embeddings using sentence-transformers (local inference)
        self.embeddings = SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2",
            device="cpu"
        )
        
        # Configure text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        
        # Initialize vector store
        self._client = None
        self._vector_store = None
        self.initialize_vector_store()
        
        self.logger.startup("Document processor initialized.")

    def initialize_vector_store(self):
        """Initialize the vector store."""
        try:
            # Initialize ChromaDB client
            self._client = chromadb.PersistentClient(
                path=str(self.vector_store_path),
                settings=Settings(anonymized_telemetry=False)
            )
            
            # Create embedding function wrapper for LangChain embeddings
            embedding_function = self.embeddings
            
            # Get or create collection
            self._vector_store = self._client.get_or_create_collection(
                name="documents",
                embedding_function=embedding_function,
                metadata={"hnsw:space": "cosine"}
            )
            
            self.logger.success("Vector store initialized.")
            
        except Exception as e:
            self.logger.error(f"Error initializing vector store: {str(e)}")
            self._vector_store = None
            raise

    def _determine_category(self, filename: str, content: str = "") -> str:
        """Determine document category based on filename and content."""
        filename_lower = filename.lower()
        
        # Technical Documentation
        if any(term in filename_lower for term in ["readme", "guide", "manual", "documentation", "api", "spec", "reference"]):
            return "Technical Documentation"
            
        # Training & Education
        elif any(term in filename_lower for term in ["training", "course", "study guide", "tutorial", "lesson", "educational"]):
            return "Training & Education"
            
        # Legal & Compliance
        elif any(term in filename_lower for term in ["epa", "section 608", "policy", "regulation", "compliance", "legal", "agreement"]):
            return "Legal & Compliance"
            
        # Reports & Analysis
        elif any(term in filename_lower for term in ["report", "analysis", "review", "assessment", "evaluation", "metrics"]):
            return "Reports & Analysis"
            
        # Project Management
        elif any(term in filename_lower for term in ["project", "plan", "roadmap", "timeline", "milestone", "sprint", "backlog"]):
            return "Project Management"
            
        # User Data & Profiles
        elif any(term in filename_lower for term in ["user", "profile", "account", "customer", "client", "candidate"]):
            return "User Data & Profiles"
            
        # Medical & Healthcare
        elif any(term in filename_lower for term in ["clinical", "patient", "medical", "health", "diagnosis", "treatment"]):
            return "Medical & Healthcare"
            
        # Templates & Forms
        elif any(term in filename_lower for term in ["template", "form", "worksheet", "checklist", "questionnaire"]):
            return "Templates & Forms"
            
        # Research & Development
        elif any(term in filename_lower for term in ["research", "experiment", "study", "investigation", "findings", "development"]):
            return "Research & Development"
            
        # Standard Operating Procedures
        elif any(term in filename_lower for term in ["sop", "procedure", "protocol", "process", "workflow", "instruction"]):
            return "Standard Operating Procedures"
        
        # Try to determine from file extension for specific file types
        ext = Path(filename).suffix.lower()
        if ext in ['.pdf', '.docx', '.doc', '.txt', '.md']:
            content_lower = content.lower()
            
            # Additional content-based categorization
            if any(term in content_lower for term in ["confidential", "private", "sensitive", "classified"]):
                return "Confidential Documents"
            elif any(term in content_lower for term in ["meeting", "minutes", "agenda", "discussion"]):
                return "Meeting Notes & Minutes"
            elif any(term in content_lower for term in ["contract", "agreement", "terms", "conditions"]):
                return "Contracts & Agreements"
        
        return "Miscellaneous"

    def get_available_categories(self) -> List[str]:
        """Get list of categories from currently stored documents."""
        try:
            if self._vector_store is None:
                self.initialize_vector_store()
            
            # Get all documents
            results = self._vector_store.get()
            if not results or not results['metadatas']:
                return []
            
            # Extract unique categories
            categories = set()
            for metadata in results['metadatas']:
                category = metadata.get('category')
                if category:
                    categories.add(category)
            
            return sorted(list(categories))
            
        except Exception as e:
            self.logger.error(f"Error getting categories: {str(e)}")
            return []

    def process_document(self, file_path: str, filename: str) -> Optional[Dict]:
        """Process a document and store it in the vector database."""
        try:
            if self._vector_store is None:
                self.initialize_vector_store()
                
            self.logger.document_process("Processing document...")
            
            # Get file size
            file_size = Path(file_path).stat().st_size
            
            # Load document
            loader = self._get_document_loader(file_path)
            if loader is None:
                self.logger.error(f"Unsupported file type: {Path(file_path).suffix}")
                return None
                
            document = loader.load()[0]
            
            # Store original content in metadata directory
            content_path = self.documents_path / f"{Path(filename).stem}_content.txt"
            with open(content_path, "w", encoding="utf-8") as f:
                f.write(document.page_content)
            
            # Determine category
            category = self._determine_category(filename, document.page_content)
            
            # Generate document ID
            doc_id = str(uuid.uuid4())
            
            # Split document
            splits = self.text_splitter.split_documents([document])
            
            # Process chunks
            chunk_ids = []
            chunk_texts = []
            chunk_metadatas = []
            
            # Disable tqdm output to terminal
            with tqdm(total=len(splits), desc="Chunks", file=open(os.devnull, 'w')) as pbar:
                for i, split in enumerate(splits):
                    chunk_id = f"{doc_id}_chunk_{i}"
                    chunk_ids.append(chunk_id)
                    chunk_texts.append(split.page_content)
                    
                    metadata = {
                        "document_id": doc_id,
                        "filename": filename,
                        "file_size": file_size,
                        "file_type": Path(file_path).suffix.lower()[1:],
                        "added_date": datetime.now().isoformat(),
                        "chunk_index": i,
                        "total_chunks": len(splits),
                        "category": category,
                        "content_path": str(content_path)
                    }
                    chunk_metadatas.append(metadata)
                    pbar.update(1)
            
            # Add to vector store using ChromaDB's native interface
            self._vector_store.add(
                ids=chunk_ids,
                documents=chunk_texts,
                metadatas=chunk_metadatas
            )
            
            self.logger.success(f"Document processed: {filename}")
            return {
                'id': doc_id,
                'filename': filename,
                'file_size': file_size,
                'file_type': Path(file_path).suffix.lower()[1:],
                'category': category,
                'added_date': datetime.now().isoformat(),
                'content_path': str(content_path)
            }
            
        except Exception as e:
            self.logger.error(f"Error processing document {filename}: {str(e)}")
            return None

    def _get_document_loader(self, file_path: str):
        """Get appropriate document loader based on file type."""
        file_ext = Path(file_path).suffix.lower()
        
        loaders = {
            '.pdf': PDFMinerLoader,
            '.txt': TextLoader,
            '.md': UnstructuredMarkdownLoader,
            '.docx': Docx2txtLoader
        }
        
        loader_class = loaders.get(file_ext)
        if loader_class:
            return loader_class(file_path)
        return None

    def get_relevant_chunks(self, query: str, num_chunks: int = 5) -> List[Dict[str, Any]]:
        """Retrieve relevant document chunks for a query."""
        try:
            if self._vector_store is None:
                self.initialize_vector_store()
                
            query_embedding = self.embeddings.encode([query])[0]
            results = self._vector_store.query(
                query_embeddings=[query_embedding],
                n_results=num_chunks,
                include=["documents", "metadatas", "distances"]
            )
            
            return [{
                'content': doc,
                'metadata': meta,
                'score': 1 - dist  # Convert distance to similarity score
            } for doc, meta, dist in zip(
                results['documents'][0],
                results['metadatas'][0],
                results['distances'][0]
            )]
            
        except Exception as e:
            self.logger.error(f"Error retrieving chunks: {str(e)}")
            return []

    def list_documents(self) -> List[Dict]:
        """List all uploaded documents."""
        try:
            if self._vector_store is None:
                self.initialize_vector_store()
            
            results = self._vector_store.get()
            if not results or not results['documents']:
                return []
            
            # Group by document_id to get unique documents
            unique_docs = {}
            for metadata in results['metadatas']:
                doc_id = metadata.get('document_id')
                if doc_id and doc_id not in unique_docs:
                    unique_docs[doc_id] = {
                        'id': doc_id,
                        'filename': metadata.get('filename'),
                        'file_size': metadata.get('file_size'),
                        'file_type': metadata.get('file_type'),
                        'added_date': metadata.get('added_date'),
                        'category': metadata.get('category', 'Uncategorized')
                    }
            
            return list(unique_docs.values())
            
        except Exception as e:
            self.logger.error(f"Error listing documents: {str(e)}")
            return []

    def get_available_categories(self) -> List[str]:
        """Get list of categories from currently stored documents."""
        try:
            documents = self.list_documents()
            if not documents:
                return []
            
            # Extract unique categories
            categories = set()
            for doc in documents:
                category = doc.get('category')
                if category:
                    categories.add(category)
            
            return sorted(list(categories))
            
        except Exception as e:
            self.logger.error(f"Error getting categories: {str(e)}")
            return []

    def delete_document(self, doc_id: str) -> bool:
        """Delete a document from the vector store."""
        try:
            if self._vector_store is None:
                self.initialize_vector_store()
            
            # Find all chunks for this document
            results = self._vector_store.get(
                where={"document_id": doc_id}
            )
            
            if results and results['ids']:
                self._vector_store.delete(
                    ids=results['ids']
                )
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error deleting document: {str(e)}")
            return False

    def _cleanup_vector_store(self):
        """Clean up vector store resources."""
        try:
            if self._client is not None:
                self._client.delete_collection("documents")
                self._vector_store = None
                self._client = None
            return True
        except Exception as e:
            self.logger.error(f"Error cleaning up vector store: {str(e)}")
            return False

    def clear_all_documents(self) -> bool:
        """Clear all documents from the vector store."""
        try:
            if self._vector_store is None:
                self.initialize_vector_store()
            
            success = self._cleanup_vector_store()
            if success:
                # Reinitialize the vector store
                self.initialize_vector_store()
                self.logger.success("All documents cleared successfully")
                return True
            return False
            
        except Exception as e:
            self.logger.error(f"Error clearing documents: {str(e)}")
            return False

    def get_document_content(self, filename: str) -> Optional[str]:
        """Get the original content of a document."""
        try:
            content_path = self.documents_path / f"{Path(filename).stem}_content.txt"
            if content_path.exists():
                with open(content_path, "r", encoding="utf-8") as f:
                    return f.read()
            return None
        except Exception as e:
            self.logger.error(f"Error getting document content: {str(e)}")
            return None
