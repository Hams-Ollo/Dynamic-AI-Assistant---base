"""
Logging configuration for the application.
"""
import logging
import sys
from typing import Union, Optional, Dict, Any

def setup_logging(config: Dict[str, Any]) -> None:
    """Configure application-wide logging.
    
    Args:
        config: Configuration dictionary containing logging settings
    """
    # Get log level from config
    level = config.get('log_level', 'INFO')
    
    # Convert string level to logging constant if needed
    if isinstance(level, str):
        level = getattr(logging, level.upper(), logging.INFO)
    
    # Basic configuration
    log_config = {
        'level': level,
        'format': '%(asctime)s - %(levelname)s - %(message)s',
        'datefmt': '%Y-%m-%d %H:%M:%S',
    }
    
    # Add file handler if log file path is specified in config
    log_file = config.get('log_file')
    if log_file:
        log_config['filename'] = log_file
        log_config['filemode'] = 'a'
    else:
        log_config['stream'] = sys.stdout
    
    # Apply configuration
    logging.basicConfig(**log_config)
    
    # Create logger
    logger = logging.getLogger(__name__)
    logger.info(f"Logging configured with level: {logging.getLevelName(level)}")
