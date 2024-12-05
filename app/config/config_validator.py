"""
Configuration Validation Module

This module provides validation for application configuration settings
and ensures all required components are properly initialized.
"""

import logging
from typing import Optional
from pathlib import Path
from dataclasses import dataclass
from .env_manager import EnvironmentManager

logger = logging.getLogger(__name__)

@dataclass
class ModelConfig:
    """Configuration for the LLM model."""
    name: str
    temperature: float
    max_tokens: int

    @classmethod
    def from_env(cls, env: EnvironmentManager) -> 'ModelConfig':
        """Create ModelConfig from environment variables."""
        return cls(
            name=env.get('MODEL_NAME'),
            temperature=env.get('MODEL_TEMPERATURE'),
            max_tokens=env.get('MODEL_MAX_TOKENS')
        )

    def validate(self) -> None:
        """Validate model configuration."""
        if not isinstance(self.temperature, float) or not 0 <= self.temperature <= 1:
            raise ValueError(f"Invalid temperature value: {self.temperature}. Must be float between 0 and 1")
        
        if not isinstance(self.max_tokens, int) or self.max_tokens <= 0:
            raise ValueError(f"Invalid max_tokens value: {self.max_tokens}. Must be positive integer")

@dataclass
class AppConfig:
    """Main application configuration."""
    env_manager: EnvironmentManager
    model_config: ModelConfig
    data_dir: Path
    log_dir: Path

    @classmethod
    def load(cls, env_file: Optional[str] = None) -> 'AppConfig':
        """Load and validate application configuration.
        
        Args:
            env_file: Optional path to .env file
            
        Returns:
            Validated AppConfig instance
        """
        # Initialize environment manager
        env_manager = EnvironmentManager(env_file)
        
        # Load model configuration
        model_config = ModelConfig.from_env(env_manager)
        
        # Set up directory paths
        project_root = Path(__file__).parent.parent.parent
        data_dir = project_root / 'data'
        log_dir = project_root / 'logs'
        
        # Create instance
        config = cls(
            env_manager=env_manager,
            model_config=model_config,
            data_dir=data_dir,
            log_dir=log_dir
        )
        
        # Validate configuration
        config.validate()
        return config

    def validate(self) -> None:
        """Validate entire application configuration."""
        # Validate model configuration
        self.model_config.validate()
        
        # Validate API keys
        if not self.env_manager.get('GROQ_API_KEY'):
            raise ValueError("GROQ_API_KEY is required")
            
        # Validate directories exist
        self._ensure_directory(self.data_dir, "Data")
        self._ensure_directory(self.log_dir, "Logs")
        
        logger.info("Configuration validation successful")

    def _ensure_directory(self, path: Path, name: str) -> None:
        """Ensure directory exists and is accessible."""
        if not path.exists():
            logger.info(f"Creating {name} directory: {path}")
            path.mkdir(parents=True, exist_ok=True)
        elif not path.is_dir():
            raise ValueError(f"{name} path exists but is not a directory: {path}")
        elif not os.access(path, os.W_OK):
            raise ValueError(f"{name} directory is not writable: {path}")
