"""
Configuration module for the RAG Ingestion Pipeline.

This module handles environment-based configuration and validation
for all required settings and secrets.
"""

import os
from typing import Optional


class Config:
    """Configuration class for the ingestion pipeline."""

    def __init__(self):
        # API Keys and Endpoints
        self.cohere_api_key: str = self._get_required_env("COHERE_API_KEY")
        self.qdrant_url: str = self._get_required_env("QDRANT_URL")
        self.qdrant_api_key: str = self._get_required_env("QDRANT_API_KEY")

        # Application settings
        self.base_url: str = os.getenv("BASE_URL", "https://physical-ai-humanoid-robotics-lovat.vercel.app/")
        self.chunk_size: int = int(os.getenv("CHUNK_SIZE", "750"))
        self.collection_name: str = os.getenv("QDRANT_COLLECTION_NAME", "rag_documents")

        # Optional settings with defaults
        user_agent_val = os.getenv("USER_AGENT", "RAG-Ingestion-Pipeline/1.0")
        self.user_agent: str = user_agent_val.strip() if user_agent_val else "RAG-Ingestion-Pipeline/1.0"

        request_timeout_val = os.getenv("REQUEST_TIMEOUT", "30")
        self.request_timeout: int = int(request_timeout_val.strip()) if request_timeout_val and request_timeout_val.strip() else 30

        crawl_delay_val = os.getenv("CRAWL_DELAY", "0.1")
        self.crawl_delay: float = float(crawl_delay_val.strip()) if crawl_delay_val and crawl_delay_val.strip() else 0.1

        max_retries_val = os.getenv("MAX_RETRIES", "3")
        self.max_retries: int = int(max_retries_val.strip()) if max_retries_val and max_retries_val.strip() else 3

        # Validate configuration values
        self._validate()

    def _get_required_env(self, key: str) -> str:
        """Get a required environment variable or raise an error."""
        value = os.getenv(key)
        if not value:
            raise ValueError(f"Required environment variable {key} is not set")
        return value

    def _validate(self):
        """Validate configuration values."""
        if self.chunk_size < 100 or self.chunk_size > 2000:
            raise ValueError("CHUNK_SIZE must be between 100 and 2000 tokens")

        if not self.base_url.startswith(('http://', 'https://')):
            raise ValueError("BASE_URL must be a valid URL starting with http:// or https://")

        if not self.qdrant_url.startswith(('http://', 'https://')):
            raise ValueError("QDRANT_URL must be a valid URL starting with http:// or https://")

    def get_cohere_config(self) -> dict:
        """Get configuration specifically for Cohere client."""
        return {
            'model': 'embed-english-v3.0',
            'input_type': 'search_document'
        }

    def get_qdrant_config(self) -> dict:
        """Get configuration specifically for Qdrant client."""
        return {
            'collection_name': self.collection_name,
            'vector_size': 1024,  # Cohere v3.0 embeddings are 1024-dimensional
            'distance': 'cosine'
        }

    def get_crawler_config(self) -> dict:
        """Get configuration specifically for web crawler."""
        return {
            'user_agent': self.user_agent,
            'timeout': self.request_timeout,
            'delay': self.crawl_delay,
            'max_retries': self.max_retries
        }


# Global config instance (will be initialized on first use)
_config_instance = None


def get_config() -> Config:
    """Get the global configuration instance, creating it if needed."""
    global _config_instance
    if _config_instance is None:
        _config_instance = Config()
    return _config_instance