# Data Model: FastAPI Integration for RAG Chatbot

**Feature**: 4-fastapi-integration
**Date**: 2025-12-26

## QueryRequest Entity

### Description
Represents a user query with optional contextual information for the RAG agent.

### Fields
- `question` (str)
  - Type: String
  - Required: Yes
  - Constraints: min_length=3, max_length=1000
  - Description: The main question text from the user

- `selected_text` (Optional[str])
  - Type: String, nullable
  - Required: No
  - Default: None
  - Description: Optional selected text that provides context for the query

- `top_k` (int)
  - Type: Integer
  - Required: No
  - Default: 5
  - Constraints: ge=1, le=20
  - Description: Number of chunks to retrieve from the knowledge base

- `min_score` (float)
  - Type: Float
  - Required: No
  - Default: 0.3
  - Constraints: ge=0.0, le=1.0
  - Description: Minimum relevance score for retrieved chunks

### Validation Rules
- Question must be 3-1000 characters
- top_k must be between 1 and 20
- min_score must be between 0.0 and 1.0
- All fields are validated using Pydantic

### Relationships
- Maps directly to RAG agent query parameters
- Provides context for the RAG agent processing

## QueryResponse Entity

### Description
Represents the response from the RAG agent with grounded information and source citations.

### Fields
- `content` (str)
  - Type: String
  - Required: Yes
  - Description: The generated response content from the RAG agent

- `sources` (List[str])
  - Type: List of strings
  - Required: Yes
  - Description: List of source URLs cited in the response

- `grounded` (bool)
  - Type: Boolean
  - Required: Yes
  - Description: Whether the response is grounded in retrieved content

- `retrieved_chunks` (List[dict])
  - Type: List of dictionaries
  - Required: Yes
  - Description: Details of retrieved chunks with metadata (chunk_id, content, source_url, page_title, section_heading, chunk_index, score, original_chunk_id)

### Validation Rules
- All fields are required
- Sources must be a list of URLs
- Grounded must be a boolean value
- Retrieved chunks must contain required metadata fields

### Relationships
- Maps from RAG agent response format
- Provides complete response information to frontend

## ErrorResponse Entity

### Description
Represents error conditions with appropriate error messages for frontend handling.

### Fields
- `error` (str)
  - Type: String
  - Required: Yes
  - Description: Error type identifier or category

- `message` (str)
  - Type: String
  - Required: Yes
  - Description: Human-readable error description

### Validation Rules
- Both fields are required
- Error and message must be non-empty strings
- Message should be safe to display to users

### Relationships
- Maps to HTTP error responses
- Provides structured error information to frontend

## State Transitions

### QueryRequest
- State: Validated → Processed by RAG agent
- Trigger: POST to /chat endpoint
- Action: Forward to RAG agent for processing

### QueryResponse
- State: Processing → Complete
- Trigger: RAG agent returns response
- Action: Format response and return to client

### ErrorResponse
- State: Error occurred → Error response prepared
- Trigger: Exception during processing
- Action: Format error and return appropriate status code