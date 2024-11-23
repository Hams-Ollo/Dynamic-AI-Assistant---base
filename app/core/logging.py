"""
Logging configuration for the application.
"""
import logging
import sys
from typing import Union, Optional

def setup_logging(level: Union[str, int] = logging.INFO, 
                 log_file: Optional[str] = None) -> None:
    """Configure application-wide logging.
    
    Args:
        level: The logging level (default: INFO)
        log_file: Optional path to log file. If not provided, logs to stdout.
    """
    # Convert string level to logging constant if needed
    if isinstance(level, str):
        level = getattr(logging, level.upper(), logging.INFO)
    
    # Basic configuration
    config = {
        'level': level,
        'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        'datefmt': '%Y-%m-%d %H:%M:%S',
    }
    
    # Add file handler if log_file is specified
    if log_file:
        config['filename'] = log_file
        config['filemode'] = 'a'
    else:
        config['stream'] = sys.stdout
    
    # Apply configuration
    logging.basicConfig(**config)
    
    # Create logger
    logger = logging.getLogger(__name__)
    logger.info(f"Logging configured with level: {logging.getLevelName(level)}")
