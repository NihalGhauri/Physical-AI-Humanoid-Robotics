# Data Model: RAG Ingestion Pipeline

## Text Chunk Entity

**Description**: Represents a segment of extracted text content with metadata and vector embedding

**Fields**:
- `chunk_id` (string): Unique identifier for the chunk, deterministically generated
- `content` (string): Text content of the chunk (500-1000 tokens)
- `source_url` (string): URL of the source page where the content was found
- `page_title` (string): Title of the source page
- `section_heading` (string): Nearest heading (h2/h3) to the content in the page
- `chunk_index` (integer): Position of the chunk within the page (0-based)
- `embedding` (list[float]): Vector representation of the content (from Cohere embedding)

## Crawled Page Entity

**Description**: Represents a web page from the Docusaurus book that has been crawled

**Fields**:
- `url` (string): URL of the page
- `title` (string): Title of the page (from HTML title tag or h1)
- `content` (string): Raw text content extracted from the page
- `headings` (list[dict]): List of headings found on the page with structure {level: int, text: string, position: int}
- `links` (list[string]): List of internal links found on the page

## Embedding Configuration

**Description**: Configuration for generating embeddings

**Fields**:
- `model` (string): Embedding model to use (e.g., embed-english-v3.0)
- `input_type` (string): Type of input (e.g., 'search_document', 'search_query')
- `truncate` (string): How to handle long inputs ('start', 'end', or null)

## Storage Configuration

**Description**: Configuration for vector storage in Qdrant

**Fields**:
- `collection_name` (string): Name of the Qdrant collection
- `vector_size` (integer): Dimension of the embedding vectors
- `metadata_schema` (dict): Schema for metadata fields
- `distance_metric` (string): Distance metric for similarity search ('Cosine', 'Euclidean', etc.)