#!/usr/bin/env python3
"""
RAG Retrieval Pipeline Validation

This script validates that the RAG ingestion pipeline successfully stored vectors
in Qdrant and can retrieve relevant content based on user queries.
"""

import os
import logging
from typing import List, Dict, Any
import cohere
from qdrant_client import QdrantClient
from qdrant_client.http import models
from dotenv import load_dotenv
import numpy as np
from dataclasses import dataclass


# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class RetrievedChunk:
    """Represents a retrieved text chunk with metadata."""
    chunk_id: str
    content: str
    source_url: str
    page_title: str
    section_heading: str
    chunk_index: int
    score: float
    original_chunk_id: str


class RetrievalValidator:
    """Validates the retrieval functionality of the RAG pipeline."""

    def __init__(self):
        # Load configuration from environment
        self.cohere_api_key = os.getenv("COHERE_API_KEY")
        self.qdrant_url = os.getenv("QDRANT_URL")
        self.qdrant_api_key = os.getenv("QDRANT_API_KEY")
        self.collection_name = os.getenv("QDRANT_COLLECTION_NAME", "Rag_Chatbot_book")

        # Validate required configuration
        if not self.cohere_api_key:
            raise ValueError("COHERE_API_KEY environment variable is required")
        if not self.qdrant_url:
            raise ValueError("QDRANT_URL environment variable is required")
        if not self.qdrant_api_key:
            raise ValueError("QDRANT_API_KEY environment variable is required")

        # Initialize clients
        self.cohere_client = cohere.Client(self.cohere_api_key)
        self.qdrant_client = QdrantClient(url=self.qdrant_url, api_key=self.qdrant_api_key, timeout=10)

        logger.info(f"Initialized retrieval validator for collection: {self.collection_name}")

    def validate_connection(self) -> bool:
        """Validate connection to Qdrant and check if collection exists."""
        try:
            # Check if collection exists
            collection_info = self.qdrant_client.get_collection(self.collection_name)
            logger.info(f"Collection {self.collection_name} exists with {collection_info.points_count} vectors")

            # Verify we can count the vectors
            count = self.qdrant_client.count(collection_name=self.collection_name)
            logger.info(f"Total vectors in collection: {count.count}")

            return count.count > 0
        except Exception as e:
            logger.error(f"Connection validation failed: {str(e)}")
            return False

    def generate_query_embedding(self, query: str) -> List[float]:
        """Generate embedding for a user query using Cohere."""
        try:
            response = self.cohere_client.embed(
                texts=[query],
                model="embed-english-v3.0",
                input_type="search_query"
            )
            return response.embeddings[0]
        except Exception as e:
            logger.error(f"Failed to generate query embedding: {str(e)}")
            return None

    def retrieve_chunks(self, query: str, top_k: int = 5) -> List[RetrievedChunk]:
        """Retrieve top-k relevant chunks for a given query."""
        logger.info(f"Retrieving top {top_k} chunks for query: '{query}'")

        # Generate embedding for the query
        query_embedding = self.generate_query_embedding(query)
        if query_embedding is None:
            logger.error("Failed to generate query embedding")
            return []

        try:
            # Query in Qdrant using the query_points method for vector search
            search_results = self.qdrant_client.query_points(
                collection_name=self.collection_name,
                query=query_embedding,
                limit=top_k
            )

            # Convert results to RetrievedChunk objects
            # query_points returns a named tuple with points
            retrieved_chunks = []
            for result in search_results.points:  # Access the points attribute
                payload = result.payload
                chunk = RetrievedChunk(
                    chunk_id=str(result.id),
                    content=payload.get('content', ''),
                    source_url=payload.get('source_url', ''),
                    page_title=payload.get('page_title', ''),
                    section_heading=payload.get('section_heading', ''),
                    chunk_index=payload.get('chunk_index', 0),
                    score=result.score,
                    original_chunk_id=payload.get('original_chunk_id', '')
                )
                retrieved_chunks.append(chunk)

            logger.info(f"Successfully retrieved {len(retrieved_chunks)} chunks")
            return retrieved_chunks

        except Exception as e:
            logger.error(f"Retrieval failed: {str(e)}")
            return []

    def validate_metadata_integrity(self, chunks: List[RetrievedChunk]) -> bool:
        """Validate that retrieved chunks have proper metadata."""
        if not chunks:
            logger.error("No chunks to validate")
            return False

        all_valid = True
        for i, chunk in enumerate(chunks):
            # Check that required metadata fields are present
            if not chunk.source_url:
                logger.warning(f"Chunk {i} missing source_url")
                all_valid = False
            if not chunk.page_title:
                logger.warning(f"Chunk {i} missing page_title")
                all_valid = False
            if chunk.chunk_index is None:
                logger.warning(f"Chunk {i} missing chunk_index")
                all_valid = False
            if not chunk.original_chunk_id:
                logger.warning(f"Chunk {i} missing original_chunk_id")
                all_valid = False

        if all_valid:
            logger.info("All retrieved chunks have complete metadata")
        else:
            logger.warning("Some chunks have missing metadata")

        return all_valid

    def validate_content_relevance(self, query: str, chunks: List[RetrievedChunk]) -> float:
        """Validate that retrieved content is relevant to the query."""
        if not chunks:
            return 0.0

        # Simple keyword matching as a basic relevance check
        query_lower = query.lower()
        relevant_chunks = 0

        for chunk in chunks:
            content_lower = chunk.content.lower()
            if any(keyword in content_lower for keyword in query_lower.split()[:3]):  # Check first 3 query words
                relevant_chunks += 1

        relevance_score = relevant_chunks / len(chunks)
        logger.info(f"Content relevance score: {relevance_score:.2f} ({relevant_chunks}/{len(chunks)} relevant)")
        return relevance_score

    def run_validation_tests(self) -> Dict[str, Any]:
        """Run comprehensive validation tests."""
        logger.info("Starting retrieval pipeline validation...")

        validation_results = {
            'connection_valid': False,
            'retrieval_success': False,
            'metadata_valid': False,
            'content_relevant': False,
            'retrieved_chunks_count': 0,
            'test_queries_results': {}
        }

        # Test 1: Connection validation
        validation_results['connection_valid'] = self.validate_connection()
        if not validation_results['connection_valid']:
            logger.error("Connection validation failed - stopping validation")
            return validation_results

        # Test queries for validation
        test_queries = [
            "ROS 2",
            "robotic nervous system",
            "humanoid robotics",
            "physical AI",
            "module 1"
        ]

        for query in test_queries:
            logger.info(f"Testing query: '{query}'")

            # Retrieve chunks for the query
            chunks = self.retrieve_chunks(query, top_k=3)
            validation_results['retrieved_chunks_count'] += len(chunks)

            # Validate metadata integrity
            metadata_valid = self.validate_metadata_integrity(chunks)

            # Validate content relevance
            relevance_score = self.validate_content_relevance(query, chunks)

            # Store results for this query
            validation_results['test_queries_results'][query] = {
                'chunks_retrieved': len(chunks),
                'metadata_valid': metadata_valid,
                'relevance_score': relevance_score
            }

            # If we have chunks and they're valid, mark retrieval as successful
            if chunks and metadata_valid:
                validation_results['retrieval_success'] = True
                if not validation_results['metadata_valid']:
                    validation_results['metadata_valid'] = True
                if relevance_score > 0.5:  # If at least 50% of chunks are relevant
                    validation_results['content_relevant'] = True

        # Overall validation success
        validation_results['overall_success'] = (
            validation_results['connection_valid'] and
            validation_results['retrieval_success'] and
            validation_results['metadata_valid']
        )

        return validation_results

    def print_validation_report(self, results: Dict[str, Any]):
        """Print a comprehensive validation report."""
        print("\n" + "="*60)
        print("RAG RETRIEVAL PIPELINE VALIDATION REPORT")
        print("="*60)

        print(f"Collection: {self.collection_name}")
        print(f"Connection Valid: {'OK' if results['connection_valid'] else 'FAIL'}")
        print(f"Retrieval Success: {'OK' if results['retrieval_success'] else 'FAIL'}")
        print(f"Metadata Valid: {'OK' if results['metadata_valid'] else 'FAIL'}")
        print(f"Content Relevant: {'OK' if results['content_relevant'] else 'FAIL'}")
        print(f"Total Chunks Retrieved: {results['retrieved_chunks_count']}")
        print(f"Overall Success: {'OK' if results['overall_success'] else 'FAIL'}")

        print("\nTest Query Results:")
        print("-" * 40)
        for query, query_results in results['test_queries_results'].items():
            print(f"Query: '{query}'")
            print(f"  - Chunks retrieved: {query_results['chunks_retrieved']}")
            print(f"  - Metadata valid: {'✓' if query_results['metadata_valid'] else '✗'}")
            print(f"  - Relevance score: {query_results['relevance_score']:.2f}")

        print("="*60)

    def interactive_retrieval(self):
        """Provide an interactive retrieval interface for testing."""
        print("\nInteractive Retrieval Mode")
        print("Enter queries to test retrieval (type 'quit' to exit):")

        while True:
            try:
                query = input("\nEnter your query: ").strip()
                if query.lower() in ['quit', 'exit', 'q']:
                    break

                if not query:
                    continue

                chunks = self.retrieve_chunks(query, top_k=5)

                if not chunks:
                    print("No results found for your query.")
                    continue

                print(f"\nTop {len(chunks)} results for '{query}':")
                print("-" * 50)

                for i, chunk in enumerate(chunks, 1):
                    print(f"{i}. Score: {chunk.score:.3f}")
                    print(f"   Source: {chunk.source_url}")
                    print(f"   Title: {chunk.page_title}")
                    print(f"   Section: {chunk.section_heading}")
                    print(f"   Content Preview: {chunk.content[:200]}...")
                    print()

            except KeyboardInterrupt:
                print("\nExiting interactive mode...")
                break
            except Exception as e:
                print(f"Error during retrieval: {str(e)}")


def main():
    """Main function to run the retrieval validation."""
    logger.info("Starting RAG Retrieval Pipeline Validation")

    try:
        # Initialize the validator
        validator = RetrievalValidator()

        # Run comprehensive validation tests
        results = validator.run_validation_tests()

        # Print validation report
        validator.print_validation_report(results)

        # If validation passed, offer interactive mode
        if results['overall_success']:
            print("\nValidation completed successfully!")
            print("You can now test interactive retrieval:")

            while True:
                choice = input("\nWould you like to try interactive retrieval? (y/n): ").strip().lower()
                if choice in ['y', 'yes']:
                    validator.interactive_retrieval()
                    break
                elif choice in ['n', 'no']:
                    break
                else:
                    print("Please enter 'y' for yes or 'n' for no.")
        else:
            logger.error("Validation failed - check the error messages above")
            return 1

        logger.info("RAG Retrieval Pipeline Validation completed")
        return 0

    except Exception as e:
        logger.error(f"Validation failed with error: {str(e)}")
        return 1


if __name__ == "__main__":
    exit(main())