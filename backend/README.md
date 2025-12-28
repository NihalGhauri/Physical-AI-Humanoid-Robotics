# RAG Ingestion Pipeline

A Python ingestion pipeline that crawls a deployed Docusaurus book, generates embeddings, and stores them in Qdrant Cloud.

## Overview

This pipeline performs the following steps:
1. Crawls all pages from a deployed Docusaurus site
2. Extracts and cleans text content
3. Chunks text with configurable size (500-1000 tokens)
4. Generates embeddings using Cohere API
5. Stores vectors in Qdrant with metadata (source_url, page_title, section_heading, chunk_index)

## Prerequisites

- Python 3.10 or higher
- `uv` package manager (optional, but recommended)
- Access to Cohere API (API key)
- Access to Qdrant Cloud (API key and endpoint)

## Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd <project-directory>
   ```

2. **Navigate to the backend directory**
   ```bash
   cd backend
   ```

3. **Install dependencies using uv (recommended)**
   ```bash
   uv sync
   ```

   Or install using pip:
   ```bash
   pip install -r requirements.txt
   ```

4. **Create a .env file with required environment variables**
   ```bash
   # .env
   COHERE_API_KEY=your_cohere_api_key_here
   QDRANT_URL=your_qdrant_cloud_url_here
   QDRANT_API_KEY=your_qdrant_api_key_here
   BASE_URL=https://physical-ai-humanoid-robotics-lovat.vercel.app/
   CHUNK_SIZE=750  # Tokens per chunk (between 500-1000)
   QDRANT_COLLECTION_NAME=rag_documents
   ```

## Usage

Run the ingestion pipeline:
```bash
python main.py
```

## Configuration

The pipeline can be configured using environment variables:

- `COHERE_API_KEY`: Your Cohere API key
- `QDRANT_URL`: Your Qdrant Cloud URL
- `QDRANT_API_KEY`: Your Qdrant API key
- `BASE_URL`: The URL of the Docusaurus site to crawl (default: https://physical-ai-humanoid-robotics-lovat.vercel.app/)
- `CHUNK_SIZE`: Number of tokens per chunk (default: 750)
- `QDRANT_COLLECTION_NAME`: Name of the Qdrant collection (default: rag_documents)
- `USER_AGENT`: User agent string for web requests (default: RAG-Ingestion-Pipeline/1.0)
- `REQUEST_TIMEOUT`: Request timeout in seconds (default: 30)
- `CRAWL_DELAY`: Delay between requests in seconds (default: 0.1)
- `MAX_RETRIES`: Maximum number of retries for failed requests (default: 3)

## Architecture

The pipeline is organized into the following modules:

- `main.py`: Main entry point that orchestrates the entire pipeline
- `config.py`: Handles environment-based configuration
- `crawler.py`: Crawls the Docusaurus site and extracts content
- `text_processor.py`: Cleans and chunks text content
- `embedding_generator.py`: Generates embeddings using Cohere API
- `vector_storage.py`: Stores vectors in Qdrant with metadata
- `utils.py`: Utility functions used across modules

## Features

- **Idempotent execution**: The pipeline can be re-run without creating duplicate entries
- **Configurable chunk size**: Adjust chunk size between 500-1000 tokens
- **Comprehensive metadata**: Stores source_url, page_title, section_heading, and chunk_index
- **Error handling**: Robust error handling with retries and logging
- **Rate limiting**: Respects API rate limits and server resources

## Testing

To run tests (if available):
```bash
python -m pytest tests/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

[Specify your license here]