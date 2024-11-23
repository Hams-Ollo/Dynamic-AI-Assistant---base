"""
Memory management for chat agents.
"""
from typing import Dict, Any, Optional
import logging
from pathlib import Path

from langchain.memory import ConversationBufferMemory
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

class MemoryManager:
    """Manages different types of memory for chat agents."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize memory manager with configuration."""
        self.config = config
        self.memory_type = config.get('type', 'vector')
        self.memory_path = Path(config.get('path', './data/memory'))
        
        # Ensure memory directory exists
        self.memory_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize appropriate memory system
        if self.memory_type == 'vector':
            self._init_vector_memory()
        else:
            self._init_buffer_memory()
            
        logging.info(f"Initialized {self.memory_type} memory system")
    
    def _init_vector_memory(self):
        """Initialize vector store memory."""
        try:
            # Initialize embeddings with a local model
            self.embeddings = HuggingFaceEmbeddings(
                model_name="all-MiniLM-L6-v2",
                model_kwargs={'device': 'cpu'}
            )
            
            # Initialize vector store
            self.vector_store = Chroma(
                persist_directory=str(self.memory_path),
                embedding_function=self.embeddings
            )
            
            self.memory = ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True
            )
        except Exception as e:
            logging.error(f"Failed to initialize vector memory: {str(e)}")
            raise
    
    def _init_buffer_memory(self):
        """Initialize simple buffer memory."""
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
    
    def add_documents(self, documents: list):
        """Add documents to vector store if using vector memory."""
        if self.memory_type == 'vector':
            try:
                self.vector_store.add_documents(documents)
                logging.info(f"Added {len(documents)} documents to vector store")
            except Exception as e:
                logging.error(f"Failed to add documents to vector store: {str(e)}")
                raise
    
    def get_relevant_context(self, query: str) -> Optional[str]:
        """Retrieve relevant context from vector store."""
        if self.memory_type == 'vector':
            try:
                docs = self.vector_store.similarity_search(query)
                return "\n".join(doc.page_content for doc in docs)
            except Exception as e:
                logging.error(f"Failed to retrieve context: {str(e)}")
                return None
        return None
    
    def cleanup(self):
        """Clean up memory resources."""
        if self.memory_type == 'vector':
            try:
                self.vector_store.persist()
                logging.info("Vector store persisted successfully")
            except Exception as e:
                logging.error(f"Failed to persist vector store: {str(e)}")
                raise
