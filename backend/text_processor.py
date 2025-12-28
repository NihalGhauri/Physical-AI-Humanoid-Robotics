"""
Text processing module for the RAG Ingestion Pipeline.

This module handles cleaning and chunking of extracted text content.
"""

import logging
import hashlib
import re
from typing import List, Dict, Any
from dataclasses import dataclass
from crawler import CrawledPage


logger = logging.getLogger(__name__)


@dataclass
class TextChunk:
    """Represents a text chunk with metadata and embedding."""
    chunk_id: str
    content: str
    source_url: str
    page_title: str
    section_heading: str
    chunk_index: int
    embedding: List[float] = None


class TextProcessor:
    """Handles text cleaning and chunking."""

    def __init__(self, chunk_size: int = 750):
        self.chunk_size = chunk_size
        self.logger = logger

    def process_pages(self, pages: List[CrawledPage]) -> List[TextChunk]:
        """Process a list of crawled pages and return text chunks."""
        all_chunks = []
        for page in pages:
            chunks = self.chunk_text(page)
            all_chunks.extend(chunks)

        self.logger.info(f"Processed {len(pages)} pages into {len(all_chunks)} chunks")
        return all_chunks

    def chunk_text(self, page: CrawledPage) -> List[TextChunk]:
        """Chunk the text content of a page into smaller pieces."""
        chunks = []

        # Use a more sophisticated chunking approach that respects sentence boundaries
        # and tries to maintain semantic coherence
        sentences = self._split_into_sentences(page.content)

        current_chunk = ""
        current_chunk_sentences = []
        chunk_index = 0

        for sentence in sentences:
            # Add sentence to current chunk
            test_chunk = current_chunk + " " + sentence if current_chunk else sentence
            test_chunk_word_count = len(test_chunk.split())

            # Check if adding this sentence would exceed chunk size
            if test_chunk_word_count <= self.chunk_size or not current_chunk:
                current_chunk = test_chunk
                current_chunk_sentences.append(sentence)
            else:
                # Create a chunk with current content if it's substantial
                if len(current_chunk.strip()) > 10:  # Only create chunk if substantial
                    section_heading = self._find_nearest_heading(
                        page.headings,
                        self._get_text_position(page.content, current_chunk)
                    )

                    chunk_id = self._generate_chunk_id(page.url, chunk_index)

                    chunk = TextChunk(
                        chunk_id=chunk_id,
                        content=current_chunk.strip(),
                        source_url=page.url,
                        page_title=page.title,
                        section_heading=section_heading,
                        chunk_index=chunk_index
                    )

                    chunks.append(chunk)
                    chunk_index += 1

                # Start new chunk with current sentence
                current_chunk = sentence
                current_chunk_sentences = [sentence]

        # Handle the last chunk if it has content
        if len(current_chunk.strip()) > 10:  # Only create chunk if substantial
            section_heading = self._find_nearest_heading(
                page.headings,
                self._get_text_position(page.content, current_chunk)
            )

            chunk_id = self._generate_chunk_id(page.url, chunk_index)

            chunk = TextChunk(
                chunk_id=chunk_id,
                content=current_chunk.strip(),
                source_url=page.url,
                page_title=page.title,
                section_heading=section_heading,
                chunk_index=chunk_index
            )

            chunks.append(chunk)

        self.logger.debug(f"Page {page.url} chunked into {len(chunks)} chunks")
        return chunks

    def _split_into_sentences(self, text: str) -> List[str]:
        """Split text into sentences while preserving sentence boundaries."""
        # This regex handles common sentence endings: . ! ? followed by whitespace or end of string
        # It also handles abbreviations like "Mr." "Dr." "U.S." etc. that shouldn't be sentence breaks
        sentence_endings = r'(?<!\b\w\.)(?<!\b\w\w\.)(?<!\b\w\w\w\.)(?<!\b\w\w\w\w\.)(?<!\b\w\w\w\w\w\.)[.!?]+\s+'
        sentences = re.split(sentence_endings, text)

        # Clean up sentences
        cleaned_sentences = []
        for sentence in sentences:
            cleaned = sentence.strip()
            if cleaned:  # Only add non-empty sentences
                cleaned_sentences.append(cleaned)

        return cleaned_sentences

    def _get_text_position(self, full_text: str, chunk_text: str) -> int:
        """Get the approximate word position of a chunk in the full text."""
        try:
            position = full_text.find(chunk_text)
            if position != -1:
                return len(full_text[:position].split())
        except:
            pass
        return 0

    def _find_nearest_heading(self, headings: List[Dict], position: int) -> str:
        """Find the nearest heading before the given text position."""
        if not headings:
            return "No Heading"

        # Find the heading with position <= our text position
        for heading in reversed(headings):
            if heading.get('position', 0) <= position:
                return heading['text'] or f"Section {heading['level']}"

        # If no heading found before position, return the first heading
        return headings[0]['text'] if headings else "No Heading"

    def _generate_chunk_id(self, url: str, chunk_index: int) -> str:
        """Generate a deterministic chunk ID based on URL and chunk index."""
        url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
        return f"{url_hash}_{chunk_index:04d}"

    def clean_text(self, text: str) -> str:
        """Additional text cleaning beyond what's done in the crawler."""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters that might interfere with embeddings
        text = re.sub(r'[^\w\s\.\!\?,:;\'\"-]', ' ', text)
        # Clean up multiple punctuation
        text = re.sub(r'[.!?]{2,}', '.', text)
        return text.strip()