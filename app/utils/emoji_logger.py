"""
Enhanced emoji-based logging utility with security features and rotation.
"""
import logging
import logging.handlers
import os
from datetime import datetime
from typing import Optional, Dict, Any
from pathlib import Path

class EmojiLogger:
    """Logger with emoji support for better visual debugging and security monitoring."""
    
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
        'optimization': '🔧',
        
        # Security and Validation
        'security': '🔒',
        'validation': '✔️',
        'auth': '🔑',
        'rate_limit': '⏳',
        'blocked': '🚫'
    }
    
    # Default paths
    LOG_DIR = 'logs'
    APP_LOG_FILE = 'application.log'
    SECURITY_LOG_FILE = 'security.log'

    @classmethod
    def setup_logging(cls, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Set up enhanced logging configuration with file rotation and security logging.
        
        Args:
            config: Optional configuration dictionary with custom settings
        """
        if config is None:
            config = {}
            
        # Create logs directory if it doesn't exist
        log_dir = Path(cls.LOG_DIR)
        log_dir.mkdir(parents=True, exist_ok=True)
        
        # Set up main application logger
        app_logger = logging.getLogger('emoji_logger')
        app_logger.setLevel(logging.DEBUG)
        
        # Set up security logger
        security_logger = logging.getLogger('security')
        security_logger.setLevel(logging.INFO)
        
        # Remove any existing handlers
        for logger in (app_logger, security_logger):
            for handler in logger.handlers[:]:
                logger.removeHandler(handler)
            logger.propagate = False

        # File handler for main application logs with rotation
        app_handler = logging.handlers.RotatingFileHandler(
            log_dir / cls.APP_LOG_FILE,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        app_handler.setLevel(logging.DEBUG)
        app_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        app_handler.setFormatter(app_formatter)
        app_logger.addHandler(app_handler)

        # File handler for security logs with rotation
        security_handler = logging.handlers.RotatingFileHandler(
            log_dir / cls.SECURITY_LOG_FILE,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        security_handler.setLevel(logging.INFO)
        security_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s - [%(extra_data)s]',
            defaults={'extra_data': ''}
        )
        security_handler.setFormatter(security_formatter)
        security_logger.addHandler(security_handler)

        # Console handler for both loggers
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter('%(message)s')
        console_handler.setFormatter(console_formatter)
        app_logger.addHandler(console_handler)
        security_logger.addHandler(console_handler)

    @classmethod
    def log(cls, category: str, message: str, level: str = 'info', extra: Optional[Dict[str, Any]] = None) -> None:
        """
        Log a message with an appropriate emoji based on category.
        
        Args:
            category: The category of the log message (must be in EMOJIS dict)
            message: The message to log
            level: The logging level (debug, info, warning, error, critical)
            extra: Optional extra data for security logging
        """
        # Ensure logging is set up only once
        if not hasattr(cls, '_logging_setup_done'):
            cls.setup_logging()
            cls._logging_setup_done = True
        
        emoji = cls.EMOJIS.get(category, '📝')
        timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
        formatted_message = f"[{timestamp}] {emoji} {message}"
        
        logger = logging.getLogger('emoji_logger')
        log_func = getattr(logger, level.lower(), logger.info)
        log_func(formatted_message)
        
        # Log to security logger if it's a security-related category
        if category in ('security', 'validation', 'auth', 'rate_limit', 'blocked'):
            security_logger = logging.getLogger('security')
            extra_str = str(extra) if extra else ''
            security_logger.info(
                formatted_message,
                extra={'extra_data': extra_str}
            )

    # Convenience methods for common log types
    @classmethod
    def security_alert(cls, message: str, extra: Optional[Dict[str, Any]] = None) -> None:
        """Log a security-related message."""
        cls.log('security', message, 'warning', extra)

    @classmethod
    def validation_error(cls, message: str, extra: Optional[Dict[str, Any]] = None) -> None:
        """Log a validation error."""
        cls.log('validation', message, 'error', extra)

    @classmethod
    def rate_limit_exceeded(cls, message: str, extra: Optional[Dict[str, Any]] = None) -> None:
        """Log a rate limit exceeded event."""
        cls.log('rate_limit', message, 'warning', extra)

    # Existing convenience methods
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
        cls.log('error', message, 'error')

    @classmethod
    def success(cls, message: str) -> None:
        cls.log('success', message)

    @classmethod
    def info(cls, message: str) -> None:
        cls.log('info', message)
