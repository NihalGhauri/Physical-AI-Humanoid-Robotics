"""
Utility functions for the RAG Ingestion Pipeline.

This module contains helper functions used across different modules.
"""

import logging
import time
from typing import Callable, Any
from functools import wraps


logger = logging.getLogger(__name__)


def retry_on_failure(max_retries: int = 3, delay: float = 1.0, backoff: float = 2.0):
    """
    Decorator to retry a function on failure.

    Args:
        max_retries: Maximum number of retry attempts
        delay: Initial delay between retries (in seconds)
        backoff: Multiplier for delay after each retry
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            current_delay = delay
            last_exception = None

            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries:
                        logger.warning(f"Attempt {attempt + 1} failed: {str(e)}. Retrying in {current_delay}s...")
                        time.sleep(current_delay)
                        current_delay *= backoff
                    else:
                        logger.error(f"All {max_retries} retries failed. Last error: {str(e)}")

            raise last_exception
        return wrapper
    return decorator


def time_function(func: Callable) -> Callable:
    """
    Decorator to time function execution.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logger.info(f"{func.__name__} took {end_time - start_time:.2f} seconds")
        return result
    return wrapper


def validate_url(url: str) -> bool:
    """
    Basic URL validation.
    """
    import re
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url_pattern.match(url) is not None


def sanitize_text(text: str) -> str:
    """
    Sanitize text for processing.
    """
    if not text:
        return ""

    # Remove null bytes and other control characters that might cause issues
    sanitized = ''.join(char for char in text if ord(char) >= 32 or char in '\n\r\t')
    return sanitized.strip()


def format_bytes(bytes_value: int) -> str:
    """
    Format bytes value into human-readable format.
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.2f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.2f} TB"


def get_text_length(text: str) -> tuple:
    """
    Get text length in characters and words.
    """
    char_count = len(text)
    word_count = len(text.split())
    return char_count, word_count


def chunk_list(lst: list, chunk_size: int) -> list:
    """
    Split a list into chunks of specified size.
    """
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]


def setup_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """
    Set up a logger with standard formatting.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Avoid adding handlers multiple times
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


def is_valid_embedding(embedding: list) -> bool:
    """
    Validate that an embedding is properly formatted.
    """
    if not isinstance(embedding, list) or len(embedding) == 0:
        return False

    # Check that all elements are numbers
    for item in embedding:
        if not isinstance(item, (int, float)):
            return False

    return True