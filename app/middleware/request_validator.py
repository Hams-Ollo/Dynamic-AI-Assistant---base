"""
Request Validation Middleware

Provides security middleware for validating and sanitizing incoming requests.
Implements rate limiting, size validation, and input sanitization.
"""

import logging
import time
from typing import Dict, Optional, Callable
from functools import wraps
from dataclasses import dataclass
from app.config.env_manager import EnvironmentManager

logger = logging.getLogger(__name__)
security_logger = logging.getLogger('security')

@dataclass
class RequestLimits:
    """Configuration for request limits."""
    max_size_mb: int
    timeout_seconds: int
    rate_limit_per_minute: int

class RequestValidator:
    """Validates and sanitizes incoming requests."""
    
    def __init__(self, env_manager: EnvironmentManager):
        """Initialize the request validator.
        
        Args:
            env_manager: Environment manager instance for config
        """
        self.limits = RequestLimits(
            max_size_mb=env_manager.get('MAX_REQUEST_SIZE_MB', 10),
            timeout_seconds=env_manager.get('REQUEST_TIMEOUT_SECONDS', 30),
            rate_limit_per_minute=env_manager.get('RATE_LIMIT_PER_MINUTE', 60)
        )
        self._rate_limit_store: Dict[str, list] = {}
    
    def validate_request_size(self, content_length: int) -> bool:
        """Validate request size against configured limits.
        
        Args:
            content_length: Size of the request in bytes
            
        Returns:
            bool: True if request size is within limits
        """
        max_size = self.limits.max_size_mb * 1024 * 1024
        if content_length > max_size:
            security_logger.warning(
                f"Request size {content_length} exceeds limit {max_size}"
            )
            return False
        return True
    
    def check_rate_limit(self, client_id: str) -> bool:
        """Check if client has exceeded rate limit.
        
        Args:
            client_id: Unique identifier for the client
            
        Returns:
            bool: True if client is within rate limit
        """
        now = time.time()
        minute_ago = now - 60
        
        # Clean up old entries
        if client_id in self._rate_limit_store:
            self._rate_limit_store[client_id] = [
                t for t in self._rate_limit_store[client_id]
                if t > minute_ago
            ]
        
        # Check rate limit
        requests = self._rate_limit_store.get(client_id, [])
        if len(requests) >= self.limits.rate_limit_per_minute:
            security_logger.warning(
                f"Rate limit exceeded for client {client_id}"
            )
            return False
        
        # Record request
        if client_id not in self._rate_limit_store:
            self._rate_limit_store[client_id] = []
        self._rate_limit_store[client_id].append(now)
        return True
    
    def sanitize_input(self, data: str) -> str:
        """Sanitize input data to prevent injection attacks.
        
        Args:
            data: Input string to sanitize
            
        Returns:
            str: Sanitized input string
        """
        # Basic sanitization - extend based on requirements
        sanitized = data.replace('<script>', '').replace('</script>', '')
        if sanitized != data:
            security_logger.warning("Potentially malicious content removed from input")
        return sanitized

def validate_request(validator: RequestValidator) -> Callable:
    """Decorator for request validation.
    
    Args:
        validator: RequestValidator instance
        
    Returns:
        Callable: Decorator function
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Extract request object (adjust based on your web framework)
            request = args[0] if args else None
            if not request:
                logger.error("No request object found")
                raise ValueError("Invalid request")
            
            # Validate request size
            content_length = getattr(request, 'content_length', 0)
            if not validator.validate_request_size(content_length):
                raise ValueError("Request size exceeds limit")
            
            # Check rate limit
            client_id = getattr(request, 'client', 'unknown')
            if not validator.check_rate_limit(str(client_id)):
                raise ValueError("Rate limit exceeded")
            
            # Proceed with request
            return await func(*args, **kwargs)
        return wrapper
    return decorator
