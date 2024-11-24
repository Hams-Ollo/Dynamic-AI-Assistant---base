"""
Configuration management for the application.
"""
import os
from pathlib import Path
from typing import Dict, Any, Optional

from dotenv import load_dotenv

def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """Load application configuration from environment and config files."""
    # Load environment variables
    env_path = Path('.env')
    load_dotenv(env_path if env_path.exists() else '.env.example')
    
    # Debug print
    print(f"Debug - GROQ_API_KEY loaded: {'*' * 4}{os.getenv('GROQ_API_KEY')[-4:] if os.getenv('GROQ_API_KEY') else 'Not found'}")
    
    config = {
        # Core settings
        'env': os.getenv('APP_ENV', 'development'),
        'debug': os.getenv('DEBUG', 'false').lower() == 'true',
        'log_level': os.getenv('LOG_LEVEL', 'INFO'),
        
        # API settings
        'api': {
            'host': os.getenv('API_HOST', 'localhost'),
            'port': int(os.getenv('API_PORT', '8000')),
        },
        
        # Agent settings
        'agent': {
            'api_key': os.getenv('GROQ_API_KEY', ''),
            'model': os.getenv('MODEL_NAME', 'mixtral-8x7b-32768'),
            'temperature': float(os.getenv('MODEL_TEMPERATURE', '0.7')),
        },
        
        # Memory settings
        'memory': {
            'type': os.getenv('MEMORY_TYPE', 'vector'),
            'backend': os.getenv('MEMORY_BACKEND', 'chroma'),
            'path': os.getenv('MEMORY_PATH', './data/memory'),
        }
    }
    
    return config
