"""
Basic tests for the RAG Ingestion Pipeline.

These tests verify that the pipeline components can be imported
and basic functionality works without errors.
"""

import os
import tempfile
from unittest.mock import Mock, patch
from dotenv import load_dotenv

# Load environment variables for testing
load_dotenv()

import sys
import os
sys.path.insert(0, os.getcwd())

from config import Config, get_config
from crawler import Crawler, CrawledPage
from text_processor import TextProcessor, TextChunk
from embedding_generator import EmbeddingGenerator, EmbeddingConfig
from vector_storage import VectorStorage


def test_config_loading():
    """Test that configuration loads correctly."""
    # This will raise an exception if required env vars are missing
    config = get_config()

    # Check that config has expected attributes
    assert hasattr(config, 'cohere_api_key')
    assert hasattr(config, 'qdrant_url')
    assert hasattr(config, 'qdrant_api_key')
    assert hasattr(config, 'base_url')
    assert hasattr(config, 'chunk_size')
    assert hasattr(config, 'collection_name')


def test_crawler_initialization():
    """Test crawler initialization."""
    crawler = Crawler("https://example.com")

    assert crawler.base_url == "https://example.com"
    assert hasattr(crawler, 'visited_urls')
    assert hasattr(crawler, 'session')


def test_text_processor_initialization():
    """Test text processor initialization."""
    processor = TextProcessor(chunk_size=500)

    assert processor.chunk_size == 500


def test_embedding_generator_initialization():
    """Test embedding generator initialization."""
    # Mock API key for testing
    with patch.dict(os.environ, {'COHERE_API_KEY': 'test-key'}):
        config = EmbeddingConfig()
        generator = EmbeddingGenerator('fake-api-key', config)

        assert generator.config == config


def test_text_chunk_creation():
    """Test TextChunk dataclass."""
    chunk = TextChunk(
        chunk_id="test_id",
        content="test content",
        source_url="https://example.com",
        page_title="Test Page",
        section_heading="Test Heading",
        chunk_index=0
    )

    assert chunk.chunk_id == "test_id"
    assert chunk.content == "test content"
    assert chunk.source_url == "https://example.com"
    assert chunk.page_title == "Test Page"
    assert chunk.section_heading == "Test Heading"
    assert chunk.chunk_index == 0


def test_crawled_page_creation():
    """Test CrawledPage dataclass."""
    page = CrawledPage(
        url="https://example.com",
        title="Test Page",
        content="Test content",
        headings=[],
        links=[]
    )

    assert page.url == "https://example.com"
    assert page.title == "Test Page"
    assert page.content == "Test content"


def test_text_processing():
    """Test basic text processing functionality."""
    processor = TextProcessor(chunk_size=100)

    # Create a mock page
    page = CrawledPage(
        url="https://example.com",
        title="Test Page",
        content="This is a test sentence. This is another test sentence. " * 50,  # Create longer content
        headings=[{"level": 2, "text": "Test Heading", "position": 0}],
        links=[]
    )

    # Process the page
    chunks = processor.chunk_text(page)

    # Verify we got chunks
    assert len(chunks) > 0
    assert all(isinstance(chunk, TextChunk) for chunk in chunks)

    # Verify chunks have expected properties
    for chunk in chunks:
        assert chunk.source_url == "https://example.com"
        assert chunk.page_title == "Test Page"
        assert len(chunk.content.split()) <= 100  # Check chunk size


def test_clean_text_function():
    """Test the text cleaning functionality."""
    processor = TextProcessor(chunk_size=500)

    dirty_text = "This   has   extra   spaces.\n\n\nAnd   newlines."
    clean_text = processor.clean_text(dirty_text)

    # Should have single spaces and single newlines
    assert "   " not in clean_text  # No triple spaces
    assert "\n\n\n" not in clean_text  # No triple newlines
    assert " " in clean_text  # Still has single spaces
    assert clean_text.startswith("This")
    assert clean_text.endswith("newlines.")


if __name__ == "__main__":
    # Run basic tests
    test_config_loading()
    test_crawler_initialization()
    test_text_processor_initialization()
    test_embedding_generator_initialization()
    test_text_chunk_creation()
    test_crawled_page_creation()
    test_text_processing()
    test_clean_text_function()

    print("All basic tests passed!")