"""
Configuration management for the AI Assistant
"""
import os
from pathlib import Path
from dotenv import load_dotenv

class Config:
    """Configuration class for the application."""
    
    DEFAULT_MODEL = "llama3-groq-70b-8192-tool-use-preview"
    
    def __init__(self):
        """Initialize configuration with environment variables."""
        # Load environment variables
        load_dotenv()
        
        # API Keys
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        if not self.groq_api_key:
            raise ValueError("GROQ_API_KEY environment variable is required")
            
        # Model Settings
        self.model_name = os.getenv("MODEL_NAME", self.DEFAULT_MODEL)
        print(f"Initializing config with model: {self.model_name}")  # Debug print
        self.temperature = float(os.getenv("TEMPERATURE", "0.7"))
        self.max_tokens = int(os.getenv("MAX_TOKENS", "8192"))
        
        # Document Processing
        self.chunk_size = int(os.getenv("CHUNK_SIZE", "1000"))
        self.chunk_overlap = int(os.getenv("CHUNK_OVERLAP", "200"))
        
        # Paths
        self.root_dir = Path(__file__).parent.parent.parent
        self.docs_dir = self.root_dir / "documents"
        self.db_dir = self.root_dir / "db"
        
        # Ensure directories exist
        self.docs_dir.mkdir(exist_ok=True)
        self.db_dir.mkdir(exist_ok=True)
    
    @property
    def embedding_model(self):
        """Get the embedding model name"""
        return os.getenv("EMBEDDING_MODEL", "openai")
    
    @property
    def vector_store(self):
        """Get the vector store type"""
        return os.getenv("VECTOR_STORE", "chroma")
    
    def get_model_kwargs(self):
        """Get model configuration parameters"""
        return {
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        }
    
    def get_document_kwargs(self):
        """Get document processing parameters"""
        return {
            "chunk_size": self.chunk_size,
            "chunk_overlap": self.chunk_overlap
        }
