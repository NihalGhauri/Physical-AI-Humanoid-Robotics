# Quickstart Guide: RAG Ingestion Pipeline

## Prerequisites

- Python 3.10 or higher
- `uv` package manager installed
- Access to Cohere API (API key)
- Access to Qdrant Cloud (API key and endpoint)

## Setup

1. **Clone the repository and navigate to the project directory**
   ```bash
   git clone <repository-url>
   cd <project-directory>
   ```

2. **Create the backend directory structure**
   ```bash
   mkdir -p backend
   ```

3. **Initialize the Python project with uv**
   ```bash
   cd backend
   uv init
   ```

4. **Create the .env file with required environment variables**
   ```bash
   # .env
   COHERE_API_KEY=your_cohere_api_key_here
   QDRANT_URL=your_qdrant_cloud_url_here
   QDRANT_API_KEY=your_qdrant_api_key_here
   BASE_URL=https://physical-ai-humanoid-robotics-lovat.vercel.app/
   CHUNK_SIZE=750  # Tokens per chunk (between 500-1000)
   ```

5. **Install required dependencies**
   ```bash
   uv pip install requests beautifulsoup4 cohere qdrant-client python-dotenv
   ```

## Project Structure

```
backend/
├── main.py                 # Main ingestion pipeline
├── config.py              # Configuration management
├── crawler.py             # Web crawling functionality
├── text_processor.py      # Text cleaning and chunking
├── embedding_generator.py # Cohere embedding generation
├── vector_storage.py      # Qdrant storage operations
└── utils.py               # Utility functions
```

## Running the Pipeline

1. **Execute the main pipeline**
   ```bash
   python main.py
   ```

2. **The pipeline will execute in the following order**:
   - Crawl all pages from the specified Docusaurus site
   - Extract and clean text content
   - Chunk text with configurable size
   - Generate embeddings using Cohere
   - Store vectors in Qdrant with metadata
   - Verify storage with test queries

## Verification

After running the pipeline, verify that:
- All pages from the site were crawled successfully
- Text was properly chunked and embedded
- Vectors were stored in Qdrant with correct metadata
- Test queries return expected results