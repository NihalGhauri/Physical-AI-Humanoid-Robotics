"""
Vector storage module for the RAG Ingestion Pipeline.

This module handles storage and retrieval of vectors in Qdrant.
"""

import logging
from typing import List
from qdrant_client import QdrantClient
from qdrant_client.http import models
from text_processor import TextChunk


logger = logging.getLogger(__name__)


class VectorStorage:
    """Handles storage of vectors in Qdrant."""

    def __init__(self, url: str, api_key: str, collection_name: str, vector_size: int = 1024):
        self.client = QdrantClient(url=url, api_key=api_key, timeout=10)
        self.collection_name = collection_name
        self.vector_size = vector_size
        self.logger = logger

    def setup_collection(self):
        """Set up the Qdrant collection if it doesn't exist."""
        try:
            # Check if collection exists
            collection_info = self.client.get_collection(self.collection_name)
            self.logger.info(f"Collection {self.collection_name} already exists with {collection_info.points_count} points")
        except:
            # Create collection with appropriate vector size (Cohere embeddings are 1024-dim for v3.0)
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(size=self.vector_size, distance=models.Distance.COSINE),
            )
            self.logger.info(f"Created collection {self.collection_name} with {self.vector_size}-dimensional vectors")

    def store_chunks(self, chunks: List[TextChunk]):
        """Store text chunks as vectors in Qdrant."""
        self.logger.info(f"Storing {len(chunks)} chunks in Qdrant collection {self.collection_name}")

        # Prepare points for insertion
        points = []
        for chunk in chunks:
            if chunk.embedding is None:
                self.logger.warning(f"Skipping chunk {chunk.chunk_id} without embedding")
                continue

            # Convert string ID to integer hash for Qdrant compatibility
            import hashlib
            chunk_id_int = int(hashlib.md5(chunk.chunk_id.encode()).hexdigest()[:16], 16)

            point = models.PointStruct(
                id=chunk_id_int,
                vector=chunk.embedding,
                payload={
                    "source_url": chunk.source_url,
                    "page_title": chunk.page_title,
                    "section_heading": chunk.section_heading,
                    "chunk_index": chunk.chunk_index,
                    "content": chunk.content,
                    "original_chunk_id": chunk.chunk_id  # Keep original ID in payload
                }
            )
            points.append(point)

        # Upload points to Qdrant
        if points:
            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )
            self.logger.info(f"Successfully stored {len(points)} vectors in Qdrant collection {self.collection_name}")

    def verify_storage(self) -> bool:
        """Verify that vectors were stored correctly."""
        try:
            count = self.client.count(collection_name=self.collection_name)
            self.logger.info(f"Verification: {count.count} vectors stored in collection {self.collection_name}")
            return count.count > 0
        except Exception as e:
            self.logger.error(f"Verification failed: {str(e)}")
            return False

    def search(self, query_vector: List[float], limit: int = 5) -> List[dict]:
        """Search for similar vectors in the collection."""
        try:
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=limit
            )

            return [{
                'chunk_id': result.id,
                'content': result.payload.get('content', ''),
                'source_url': result.payload.get('source_url', ''),
                'page_title': result.payload.get('page_title', ''),
                'section_heading': result.payload.get('section_heading', ''),
                'score': result.score
            } for result in results]
        except Exception as e:
            self.logger.error(f"Search failed: {str(e)}")
            return []

    def get_chunk_by_id(self, chunk_id: str) -> dict:
        """Retrieve a specific chunk by its ID."""
        try:
            records = self.client.retrieve(
                collection_name=self.collection_name,
                ids=[chunk_id]
            )

            if records:
                record = records[0]
                return {
                    'chunk_id': record.id,
                    'content': record.payload.get('content', ''),
                    'source_url': record.payload.get('source_url', ''),
                    'page_title': record.payload.get('page_title', ''),
                    'section_heading': record.payload.get('section_heading', ''),
                    'chunk_index': record.payload.get('chunk_index', 0)
                }
        except Exception as e:
            self.logger.error(f"Retrieval failed: {str(e)}")

        return None

    def delete_collection(self):
        """Delete the entire collection (use with caution)."""
        try:
            self.client.delete_collection(self.collection_name)
            self.logger.info(f"Collection {self.collection_name} deleted")
        except Exception as e:
            self.logger.error(f"Failed to delete collection: {str(e)}")

    def is_collection_empty(self) -> bool:
        """Check if the collection is empty."""
        try:
            count = self.client.count(collection_name=self.collection_name)
            return count.count == 0
        except Exception:
            return True  # If there's an error checking, assume it's not properly set up