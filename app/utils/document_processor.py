"""
Document processing and vectorization utilities.
"""
from typing import Dict, List, Optional, Any
import uuid
from datetime import datetime
import logging
from pathlib import Path
import shutil
import os
import time
import gc
from app.utils.emoji_logger import EmojiLogger

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    UnstructuredWordDocumentLoader,
    UnstructuredMarkdownLoader
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

class DocumentProcessor:
    """Handles document processing, chunking, and vectorization."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize document processor with configuration."""
        self.config = config or {}
        self.embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2"
        )
        
        # Ensure vector_store_type is set
        self.vector_store_type = self.config.get("vector_store_type", "chroma")
        if not hasattr(self, 'vector_store_type'):
            raise AttributeError("DocumentProcessor must have a 'vector_store_type' attribute")
        
        self.logger = EmojiLogger
        self.logger.startup("Document processor initialized.")
        
        # Set up persistent paths
        self.base_path = Path("data/documents")
        self.documents_path = self.base_path / "metadata"
        self.vector_store_path = self.base_path / "vector_store"
        
        # Ensure directories exist
        self.documents_path.mkdir(parents=True, exist_ok=True)
        self.vector_store_path.mkdir(parents=True, exist_ok=True)
        
        # Configure Chroma settings
        self.chroma_settings = {
            "allow_reset": True,
            "anonymized_telemetry": False
        }
        
        self.initialize_vector_store()
        
        # Configure text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        
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
            json.dump(self.documents, f, indent=2)
    
    def initialize_vector_store(self):
        """Initialize the vector store based on configuration."""
        try:
            if self.vector_store_type == "chroma":
                # Cleanup existing instance if any
                self._cleanup_vector_store()
                
                # Initialize new database with persistence and settings
                self._vector_store = Chroma(
                    persist_directory=str(self.vector_store_path),
                    embedding_function=self.embeddings,
                    client_settings=self.chroma_settings
                )
                self.logger.success("✅ Vector store initialized.")
            else:
                raise ValueError("Unsupported vector store type.")
        except Exception as e:
            self.logger.error(f"Error initializing vector store: {str(e)}")

    def set_vector_store(self, store_type: str):
        """Change the vector store type and reinitialize."""
        if store_type != self.vector_store_type:
            self.vector_store_type = store_type
            self.initialize_vector_store()
            self._load_document_metadata()

    def process_document(self, file_path: str, file_name: str) -> Optional[str]:
        """Process a document and store it in the vector database."""
        try:
            self.logger.document_process("Processing document...")
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
            self._vector_store.add_documents(chunks)
        
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
            '.docx': UnstructuredWordDocumentLoader,
            '.md': UnstructuredMarkdownLoader
        }
        
        loader_class = loaders.get(file_ext)
        return loader_class(file_path) if loader_class else None
    
    def get_relevant_chunks(self, query: str, num_chunks: int = 5) -> List[Dict[str, Any]]:
        """Retrieve relevant document chunks for a query."""
        try:
            results = self._vector_store.similarity_search_with_score(
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
    
    def list_documents(self) -> List[Dict]:
        """List all uploaded documents."""
        return list(self.documents.values())
    
    def _cleanup_vector_store(self):
        """Clean up vector store resources."""
        try:
            if hasattr(self, '_vector_store'):
                # Persist any changes
                if hasattr(self._vector_store, '_client'):
                    try:
                        self._vector_store._client.persist()
                    except Exception as e:
                        logging.warning(f"Error persisting vector store: {str(e)}")
                
                # Explicitly delete client and collection
                if hasattr(self._vector_store, '_client'):
                    try:
                        self._vector_store._client.reset()
                        delattr(self._vector_store, '_client')
                    except Exception as e:
                        logging.warning(f"Error resetting vector store client: {str(e)}")
            
            # Clear the vector store reference
            self._vector_store = None
            
            # Force garbage collection
            gc.collect()
            
            # Add a small delay to ensure resources are released
            time.sleep(0.5)
            
        except Exception as e:
            logging.error(f"Error cleaning up vector store: {str(e)}")

    def delete_document(self, doc_id: str) -> bool:
        """Delete a document from storage and vector store."""
        try:
            # Get document info before deletion
            doc_info = self.documents.get(doc_id)
            if not doc_info:
                logging.warning(f"Document {doc_id} not found")
                return False

            # Clean up vector store first
            self._cleanup_vector_store()
            
            # Remove from documents metadata
            if doc_id in self.documents:
                del self.documents[doc_id]
                self._save_document_metadata()

            # Delete the physical file if it exists
            file_path = doc_info.get('path')
            if file_path and os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except PermissionError:
                    logging.warning(f"Permission error deleting file {file_path}, will retry...")
                    time.sleep(1)  # Wait a bit and retry
                    os.remove(file_path)

            # Reinitialize vector store
            self.initialize_vector_store()
            
            return True

        except Exception as e:
            logging.error(f"Error deleting document: {str(e)}")
            return False

    def clear_all_documents(self) -> bool:
        """Clear all documents from storage."""
        try:
            # Clean up vector store first
            self._cleanup_vector_store()
            
            # Clear document metadata
            self.documents = {}
            self._save_document_metadata()
            
            # Clear vector store directory
            if self.vector_store_path.exists():
                try:
                    shutil.rmtree(self.vector_store_path)
                    self.vector_store_path.mkdir(exist_ok=True)
                except Exception as e:
                    logging.error(f"Error clearing vector store directory: {str(e)}")
                    return False
            
            # Reinitialize vector store
            self.initialize_vector_store()
            
            return True
            
        except Exception as e:
            logging.error(f"Error clearing all documents: {str(e)}")
            return False

    def clear_vector_store(self) -> bool:
        """Clear all documents from the vector store and reset metadata."""
        try:
            logging.info("Clearing vector store and metadata...")
            
            # First cleanup existing vector store
            self._cleanup_vector_store()
            
            # Delete the entire vector store directory
            if self.vector_store_path.exists():
                shutil.rmtree(self.vector_store_path)
            
            # Reset metadata file
            metadata_file = self.documents_path / "documents.json"
            if metadata_file.exists():
                metadata_file.unlink()
            
            # Reset internal state
            self.documents = {}
            self._save_document_metadata()
            
            # Reinitialize empty vector store
            self.initialize_vector_store()
            
            logging.info("Successfully cleared vector store and metadata")
            return True
            
        except Exception as e:
            logging.error(f"Error clearing vector store: {str(e)}")
            return False
