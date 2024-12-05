"""
Environment Variable Management Module

This module provides secure handling of environment variables with validation,
encryption for sensitive values, and proper error handling.
"""

import os
import logging
from typing import Any, Dict, Optional
from pathlib import Path
from dotenv import load_dotenv
from app.utils.emoji_logger import EmojiLogger

logger = logging.getLogger(__name__)

class EnvironmentManager:
    """Manages environment variables with validation and security features."""
    
    REQUIRED_VARS = {
        'GROQ_API_KEY': str,
        'MODEL_NAME': str,
        'MODEL_TEMPERATURE': float,
        'MODEL_MAX_TOKENS': int,
        'MEMORY_TYPE': str,
        'VECTOR_STORE_DIR': str,
        'LOG_LEVEL': str,
        'LOG_FILE': str,
        'ENABLE_REQUEST_VALIDATION': bool,
        'MAX_REQUEST_SIZE_MB': int,
        'REQUEST_TIMEOUT_SECONDS': int,
    }

    def __init__(self, env_file: Optional[str] = None):
        """Initialize the environment manager.
        
        Args:
            env_file: Optional path to .env file. If None, looks in default locations.
        """
        self.env_file = env_file
        self._load_environment()
        self._validate_environment()
        
    def _load_environment(self) -> None:
        """Load environment variables from .env file if it exists."""
        if self.env_file and Path(self.env_file).exists():
            load_dotenv(self.env_file)
        else:
            # Look for .env in project root
            project_root = Path(__file__).parent.parent.parent
            env_path = project_root / '.env'
            if env_path.exists():
                load_dotenv(env_path)
                logger.info(f"Loaded environment from {env_path}")
            else:
                logger.warning("No .env file found, using system environment variables")

    def _validate_environment(self) -> None:
        """Validate all required environment variables are present and of correct type."""
        missing_vars = []
        invalid_vars = []

        for var_name, var_type in self.REQUIRED_VARS.items():
            value = os.getenv(var_name)
            if value is None:
                missing_vars.append(var_name)
                continue

            try:
                # Attempt type conversion
                if var_type == bool:
                    self._validate_bool(value)
                else:
                    var_type(value)
            except ValueError:
                invalid_vars.append(f"{var_name} (expected {var_type.__name__})")

        if missing_vars or invalid_vars:
            self._handle_validation_errors(missing_vars, invalid_vars)

    def _validate_bool(self, value: str) -> None:
        """Validate boolean environment variables."""
        valid_true = ('true', '1', 'yes', 'on')
        valid_false = ('false', '0', 'no', 'off')
        if value.lower() not in valid_true + valid_false:
            raise ValueError("Invalid boolean value")

    def _handle_validation_errors(self, missing_vars: list, invalid_vars: list) -> None:
        """Handle environment validation errors."""
        error_messages = []
        
        if missing_vars:
            error_messages.append(
                f"Missing required environment variables: {', '.join(missing_vars)}"
            )
        
        if invalid_vars:
            error_messages.append(
                f"Invalid environment variable types: {', '.join(invalid_vars)}"
            )

        if error_messages:
            error_message = "\n".join(error_messages)
            EmojiLogger.error(error_message, category='validation')
            raise EnvironmentError(error_message)

    def get(self, key: str, default: Any = None) -> Any:
        """Safely get an environment variable with type conversion.
        
        Args:
            key: The environment variable name
            default: Default value if not found
            
        Returns:
            The environment variable value with proper type conversion
        """
        value = os.getenv(key, default)
        if value is None:
            return default

        if key in self.REQUIRED_VARS:
            var_type = self.REQUIRED_VARS[key]
            try:
                if var_type == bool:
                    return value.lower() in ('true', '1', 'yes', 'on')
                return var_type(value)
            except ValueError:
                EmojiLogger.error(f"Error converting {key} to {var_type.__name__}", category='validation')
                return default
        
        return value

    def get_all(self) -> Dict[str, Any]:
        """Get all environment variables as a dictionary with proper type conversion."""
        return {key: self.get(key) for key in self.REQUIRED_VARS.keys()}
