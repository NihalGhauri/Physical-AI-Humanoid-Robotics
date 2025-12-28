"""
Embedding generation module for the RAG Ingestion Pipeline.

This module handles generation of embeddings using the Cohere API.
"""

import logging
import time
from typing import List
from dataclasses import dataclass
import cohere
from text_processor import TextChunk


logger = logging.getLogger(__name__)


@dataclass
class EmbeddingConfig:
    """Configuration for embedding generation."""
    model: str = "embed-english-v3.0"
    input_type: str = "search_document"
    truncate: str = "END"


class EmbeddingGenerator:
    """Handles generation of embeddings using Cohere API."""

    def __init__(self, api_key: str, config: EmbeddingConfig = None):
        self.client = cohere.Client(api_key)
        self.config = config or EmbeddingConfig()
        self.logger = logger

    def generate_embeddings(self, chunks: List[TextChunk]) -> List[TextChunk]:
        """Generate embeddings for a list of text chunks."""
        self.logger.info(f"Generating embeddings for {len(chunks)} chunks using model {self.config.model}")

        if not chunks:
            self.logger.warning("No chunks to generate embeddings for")
            return chunks

        # Extract text content for batch processing
        texts = [chunk.content for chunk in chunks]

        # Generate embeddings in batches to respect API limits
        batch_size = 96  # Cohere's max batch size
        all_embeddings = []

        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]

            try:
                response = self.client.embed(
                    texts=batch,
                    model=self.config.model,
                    input_type=self.config.input_type,
                    truncate=self.config.truncate
                )

                all_embeddings.extend(response.embeddings)
                self.logger.debug(f"Processed batch {i//batch_size + 1}/{(len(texts)-1)//batch_size + 1}")

                # Be respectful to the API - add delay between requests
                time.sleep(0.1)

            except Exception as e:
                self.logger.error(f"Error generating embeddings for batch {i//batch_size + 1}: {str(e)}")
                # Fill with None embeddings to maintain alignment
                all_embeddings.extend([None] * len(batch))

        # Update chunks with embeddings
        successful_embeddings = 0
        for i, chunk in enumerate(chunks):
            if i < len(all_embeddings) and all_embeddings[i] is not None:
                chunk.embedding = all_embeddings[i]
                successful_embeddings += 1
            else:
                self.logger.warning(f"Failed to generate embedding for chunk {chunk.chunk_id}")

        self.logger.info(f"Successfully generated {successful_embeddings}/{len(chunks)} embeddings")
        return chunks

    def generate_single_embedding(self, text: str) -> List[float]:
        """Generate a single embedding for a piece of text."""
        try:
            response = self.client.embed(
                texts=[text],
                model=self.config.model,
                input_type=self.config.input_type,
                truncate=self.config.truncate
            )
            return response.embeddings[0]
        except Exception as e:
            self.logger.error(f"Error generating single embedding: {str(e)}")
            return None

    def validate_embeddings(self, chunks: List[TextChunk]) -> List[TextChunk]:
        """Validate that all chunks have valid embeddings."""
        valid_chunks = []
        invalid_count = 0

        for chunk in chunks:
            if chunk.embedding is None or len(chunk.embedding) == 0:
                self.logger.warning(f"Chunk {chunk.chunk_id} has invalid embedding")
                invalid_count += 1
            else:
                valid_chunks.append(chunk)

        if invalid_count > 0:
            self.logger.info(f"Found {invalid_count} chunks with invalid embeddings out of {len(chunks)} total")

        return valid_chunks