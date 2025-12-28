#!/usr/bin/env python3
"""
RAG Ingestion Pipeline - Main Entry Point

This script implements a complete ingestion pipeline that:
1. Crawls a deployed Docusaurus book
2. Extracts and cleans text content
3. Chunks text with configurable size
4. Generates embeddings using Cohere
5. Stores vectors in Qdrant with metadata
"""

import logging
from dotenv import load_dotenv
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import get_config
from crawler import Crawler
from text_processor import TextProcessor
from embedding_generator import EmbeddingGenerator, EmbeddingConfig
from vector_storage import VectorStorage
from utils import setup_logger


# Load environment variables
load_dotenv()

# Configure logging
logger = setup_logger(__name__)


def main():
    """Main function to orchestrate the ingestion pipeline."""
    logger.info("Starting RAG Ingestion Pipeline")

    try:
        # Load configuration
        config = get_config()
        logger.info("Configuration loaded successfully")

        # Initialize components
        crawler = Crawler(
            base_url=config.base_url,
            user_agent=config.user_agent,
            timeout=config.request_timeout,
            delay=config.crawl_delay,
            max_retries=config.max_retries
        )

        text_processor = TextProcessor(config.chunk_size)

        embedding_config = EmbeddingConfig()
        embedding_generator = EmbeddingGenerator(config.cohere_api_key, embedding_config)

        vector_storage = VectorStorage(
            config.qdrant_url,
            config.qdrant_api_key,
            config.collection_name
        )

        # Set up Qdrant collection
        vector_storage.setup_collection()

        # Step 1: Crawl the site
        logger.info("Starting site crawling...")
        crawled_pages = crawler.crawl_site()

        if not crawled_pages:
            logger.error("No pages were crawled. Exiting.")
            return

        # Step 2: Process and chunk text
        logger.info("Processing and chunking text...")
        all_chunks = text_processor.process_pages(crawled_pages)
        logger.info(f"Total chunks created: {len(all_chunks)}")

        # Step 3: Generate embeddings
        logger.info("Generating embeddings...")
        chunks_with_embeddings = embedding_generator.generate_embeddings(all_chunks)

        # Filter out chunks that failed to get embeddings
        valid_chunks = embedding_generator.validate_embeddings(chunks_with_embeddings)
        logger.info(f"Chunks with valid embeddings: {len(valid_chunks)}")

        # Step 4: Store vectors in Qdrant
        logger.info("Storing vectors in Qdrant...")
        vector_storage.store_chunks(valid_chunks)

        # Step 5: Verify storage
        success = vector_storage.verify_storage()

        if success:
            logger.info("RAG Ingestion Pipeline completed successfully!")
        else:
            logger.error("Pipeline completed but verification failed.")

    except Exception as e:
        logger.error(f"Pipeline failed with error: {str(e)}")
        raise


if __name__ == "__main__":
    main()