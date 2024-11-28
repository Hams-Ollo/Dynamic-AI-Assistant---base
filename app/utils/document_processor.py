"""
Document processing and vectorization utilities.
"""
from typing import Dict, List, Optional, Any
import uuid
from datetime import datetime
import logging
from pathlib import Path

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    UnstructuredWordDocumentLoader,
    UnstructuredMarkdownLoader,
    UnstructuredPowerPointLoader,
    CSVLoader,
    Docx2txtLoader,
    UnstructuredExcelLoader
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import pandas as pd

class DocumentProcessor:
    """Handles document processing, chunking, and vectorization."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize document processor with configuration."""
        self.config = config or {}
        self.embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2"
        )
        
        # Initialize vector store
        self.vector_store = Chroma(
            collection_name="uploaded_documents",
            embedding_function=self.embeddings,
            persist_directory=str(Path("data/documents"))
        )
        
        # Configure text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        
        # Document metadata storage
        self.documents_path = Path("data/documents/metadata")
        self.documents_path.mkdir(parents=True, exist_ok=True)
        
        self._load_document_metadata()
    
    def _load_document_metadata(self):
        """Load document metadata from storage."""
        self.documents = {}
        metadata_file = self.documents_path / "documents.json"
        if metadata_file.exists():
            import json
            with open(metadata_file, 'r') as f:
                self.documents = json.load(f)
    
    def _save_document_metadata(self):
        """Save document metadata to storage."""
        metadata_file = self.documents_path / "documents.json"
        import json
        with open(metadata_file, 'w') as f:
            json.dump(self.documents, f)
    
    def process_document(self, file_path: str, file_name: str) -> Optional[str]:
        """Process a document and store it in the vector database."""
        try:
            # Check for duplicate document
            for doc_id, doc in self.documents.items():
                if doc['name'] == file_name:
                    # Delete existing document
                    self.delete_document(doc_id)
                    break
            
            # Load document based on file type
            loader = self._get_document_loader(file_path)
            if not loader:
                raise ValueError(f"Unsupported file type: {file_path}")
            
            # Load and split document
            doc = loader.load()
            chunks = self.text_splitter.split_documents(doc)
            
            # Generate document ID
            doc_id = str(uuid.uuid4())
            
            # Add metadata to chunks
            for chunk in chunks:
                chunk.metadata.update({
                    "document_id": doc_id,
                    "file_name": file_name,
                    "chunk_id": str(uuid.uuid4()),
                    "timestamp": datetime.now().isoformat()
                })
            
            # Store in vector database
            self.vector_store.add_documents(chunks)
            
            # Store document metadata
            self.documents[doc_id] = {
                "id": doc_id,
                "name": file_name,
                "path": file_path,
                "timestamp": datetime.now().isoformat(),
                "num_chunks": len(chunks)
            }
            self._save_document_metadata()
            
            return doc_id
            
        except Exception as e:
            logging.error(f"Error processing document {file_name}: {str(e)}")
            raise
    
    def _get_document_loader(self, file_path: str):
        """Get appropriate document loader based on file type."""
        file_ext = Path(file_path).suffix.lower()
        
        loaders = {
            '.pdf': PyPDFLoader,
            '.txt': TextLoader,
            '.docx': Docx2txtLoader,
            '.doc': UnstructuredWordDocumentLoader,
            '.md': UnstructuredMarkdownLoader,
            '.ppt': UnstructuredPowerPointLoader,
            '.pptx': UnstructuredPowerPointLoader,
            '.xlsx': ExcelLoader,
            '.xls': ExcelLoader,
            '.csv': CSVLoader
        }
        
        loader_class = loaders.get(file_ext)
        return loader_class(file_path) if loader_class else None
    
    def get_relevant_chunks(self, query: str, num_chunks: int = 5) -> List[Dict[str, Any]]:
        """Retrieve relevant document chunks for a query."""
        try:
            results = self.vector_store.similarity_search_with_score(
                query,
                k=num_chunks
            )
            
            return [{
                'content': doc.page_content,
                'metadata': doc.metadata,
                'score': score
            } for doc, score in results]
            
        except Exception as e:
            logging.error(f"Error retrieving chunks for query: {str(e)}")
            return []
    
    def list_documents(self) -> List[Dict[str, Any]]:
        """List all uploaded documents."""
        return list(self.documents.values())
    
    def delete_document(self, doc_id: str):
        """Delete a document and its chunks from storage."""
        try:
            # Delete from vector store
            self.vector_store.delete(
                where={"document_id": doc_id}
            )
            
            # Delete metadata
            if doc_id in self.documents:
                del self.documents[doc_id]
                self._save_document_metadata()
                
        except Exception as e:
            logging.error(f"Error deleting document {doc_id}: {str(e)}")
            raise
    
    def clear_all_documents(self):
        """Clear all documents and reset storage."""
        try:
            # Clear vector store
            self.vector_store.delete(where={})
            
            # Clear metadata
            self.documents = {}
            self._save_document_metadata()
            
        except Exception as e:
            logging.error(f"Error clearing documents: {str(e)}")
            raise

class ExcelLoader:
    """Custom loader for Excel files using pandas."""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
    
    def load(self) -> List[Any]:
        """Load Excel file and convert to documents."""
        from langchain.schema import Document
        
        df = pd.read_excel(self.file_path)
        # Convert all columns to string and join them
        text = "\n".join(
            f"{col}:\n{df[col].astype(str).str.cat(sep=', ')}"
            for col in df.columns
        )
        
        return [Document(
            page_content=text,
            metadata={"source": self.file_path}
        )]
