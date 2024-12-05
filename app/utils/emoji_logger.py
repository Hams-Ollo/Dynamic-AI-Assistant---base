"""
Emoji-enhanced logging utility for better visual debugging.
"""
import logging
import os
from datetime import datetime
from typing import Optional

class EmojiLogger:
    """Logger with emoji support for better visual debugging."""
    
    # Emoji categories for different types of logs
    EMOJIS = {
        # System and Application Flow
        'startup': '🚀',
        'shutdown': '🔌',
        'config': '⚙️',
        'success': '✅',
        'error': '❌',
        'warning': '⚠️',
        'info': 'ℹ️',
        
        # Document Processing
        'document_upload': '📄',
        'document_process': '⚡',
        'document_complete': '📚',
        'embedding': '🧬',
        'vector_store': '💾',
        
        # Chat and Messaging
        'user_message': '👤',
        'ai_message': '🤖',
        'thinking': '🤔',
        'memory': '🧠',
        
        # Database and Storage
        'database': '🗄️',
        'save': '💾',
        'load': '📂',
        'delete': '🗑️',
        
        # Performance and Monitoring
        'time': '⏱️',
        'memory_usage': '📊',
        'optimization': '🔧'
    }
    
    LOG_FILE_PATH = 'logs/application.log'

    @classmethod
    def setup_logging(cls):
        """
        Set up logging configuration with file and console handlers.
        """
        # Create logs directory if it doesn't exist
        os.makedirs(os.path.dirname(cls.LOG_FILE_PATH), exist_ok=True)

        # Set up logging
        logger = logging.getLogger('emoji_logger')
        logger.setLevel(logging.DEBUG)
        
        # Remove any existing handlers
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
            
        # Prevent propagation to root logger
        logger.propagate = False

        # File handler for logging all messages
        file_handler = logging.FileHandler(cls.LOG_FILE_PATH, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

        # Console handler for logging crucial messages
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter('%(message)s')
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

    @classmethod
    def log(cls, category: str, message: str, level: str = 'info') -> None:
        """
        Log a message with an appropriate emoji based on category.
        
        Args:
            category: The category of the log message (must be in EMOJIS dict)
            message: The message to log
            level: The logging level (debug, info, warning, error, critical)
        """
        # Ensure logging is set up only once
        if not hasattr(cls, '_logging_setup_done'):
            cls.setup_logging()
            cls._logging_setup_done = True
        
        emoji = cls.EMOJIS.get(category, '📝')  # Default emoji if category not found
        timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
        formatted_message = f"[{timestamp}] {emoji} {message}"
        
        logger = logging.getLogger('emoji_logger')
        
        if level == 'debug':
            logger.debug(formatted_message)
        elif level == 'info':
            logger.info(formatted_message)
        elif level == 'warning':
            logger.warning(formatted_message)
        elif level == 'error':
            logger.error(formatted_message)
        elif level == 'critical':
            logger.critical(formatted_message)
            
    @classmethod
    def startup(cls, message: str) -> None:
        cls.log('startup', message)
        
    @classmethod
    def shutdown(cls, message: str) -> None:
        cls.log('shutdown', message)
        
    @classmethod
    def user_message(cls, message: str) -> None:
        cls.log('user_message', message)
        
    @classmethod
    def ai_message(cls, message: str) -> None:
        cls.log('ai_message', message)
        
    @classmethod
    def document_process(cls, message: str) -> None:
        cls.log('document_process', message)
        
    @classmethod
    def error(cls, message: str) -> None:
        cls.log('error', message, level='error')
        
    @classmethod
    def success(cls, message: str) -> None:
        cls.log('success', message)

    @classmethod
    def info(cls, message: str) -> None:
        cls.log('info', message)
