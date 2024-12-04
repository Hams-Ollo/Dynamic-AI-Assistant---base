"""
Configuration management for the AI Assistant
"""
import os
from pathlib import Path
from typing import Dict, Any
from dotenv import load_dotenv

class Config:
    """Configuration class for the application."""
    
    DEFAULT_MODEL = "llama3-groq-70b-8192-tool-use-preview"
    
    def __init__(self):
        """Initialize configuration with environment variables."""
        # Load environment variables
        env_path = Path('.env')
        load_dotenv(env_path if env_path.exists() else '.env.example')
        
        # Core settings
        self.env = os.getenv('APP_ENV', 'development')
        self.debug = os.getenv('DEBUG', 'false').lower() == 'true'
        self.log_level = os.getenv('LOG_LEVEL', 'INFO')
        
        # API Keys
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        if not self.groq_api_key:
            raise ValueError("GROQ_API_KEY environment variable is required")
        print(f"Debug - GROQ_API_KEY loaded: {'*' * 4}{self.groq_api_key[-4:] if self.groq_api_key else 'Not found'}")
            
        # Model Settings
        self.model_name = os.getenv("MODEL_NAME", self.DEFAULT_MODEL)
        print(f"Initializing config with model: {self.model_name}")
        self.temperature = float(os.getenv("MODEL_TEMPERATURE", "0.7"))
        self.max_tokens = int(os.getenv("MAX_TOKENS", "8192"))
        
        # API settings
        self.api_host = os.getenv('API_HOST', 'localhost')
        self.api_port = int(os.getenv('API_PORT', '8000'))
        
        # Memory settings
        self.memory_type = os.getenv('MEMORY_TYPE', 'vector')
        self.memory_backend = os.getenv('MEMORY_BACKEND', 'chroma')
        self.memory_path = os.getenv('MEMORY_PATH', './data/memory')
        
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
    def embedding_model(self) -> str:
        """Get the embedding model name"""
        return os.getenv("EMBEDDING_MODEL", "huggingface")
    
    @property
    def vector_store(self) -> str:
        """Get the vector store type"""
        return os.getenv("VECTOR_STORE", "chroma")
    
    def get_model_kwargs(self) -> Dict[str, Any]:
        """Get model configuration parameters"""
        return {
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        }
    
    def get_document_kwargs(self) -> Dict[str, Any]:
        """Get document processing parameters"""
        return {
            "chunk_size": self.chunk_size,
            "chunk_overlap": self.chunk_overlap
        }
    
    def get_api_config(self) -> Dict[str, Any]:
        """Get API configuration"""
        return {
            "host": self.api_host,
            "port": self.api_port
        }
    
    def get_memory_config(self) -> Dict[str, Any]:
        """Get memory configuration"""
        return {
            "type": self.memory_type,
            "backend": self.memory_backend,
            "path": self.memory_path
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary format"""
        return {
            "env": self.env,
            "debug": self.debug,
            "log_level": self.log_level,
            "api": self.get_api_config(),
            "agent": {
                "api_key": self.groq_api_key,
                "model": self.model_name,
                "temperature": self.temperature,
            },
            "memory": self.get_memory_config(),
            "document": self.get_document_kwargs()
        }
