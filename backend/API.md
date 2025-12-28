# RAG Chatbot API

This FastAPI backend connects the frontend chat interface with the RAG agent, enabling users to ask questions about the book and receive grounded responses.

## Features

- FastAPI endpoint for querying the RAG agent
- Support for user-selected text scope in queries
- Health check endpoints for monitoring
- Proper error handling and validation
- CORS support for frontend integration
- Stateless design (no chat history persistence)

## Requirements

- Python 3.10+
- FastAPI
- uvicorn (for running the server)
- The existing RAG agent components from `agent.py`
- Environment variables configured in `.env`

## Environment Variables

Create a `.env` file in the backend directory with the following variables:

```env
OPENAI_API_KEY=your_openai_api_key
GEMINI_API_KEY=your_gemini_api_key  # Optional - for Gemini model support
COHERE_API_KEY=your_cohere_api_key
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key
QDRANT_COLLECTION_NAME=Rag_Chatbot_book  # Optional, defaults to Rag_Chatbot_book
AGENT_TEMPERATURE=0.7  # Optional, defaults to 0.7
AGENT_MAX_TOKENS=2048  # Optional, defaults to 2048
AGENT_TOP_K=5  # Optional, defaults to 5
AGENT_MIN_SCORE=0.3  # Optional, defaults to 0.3
AGENT_MODEL_NAME=gemini-2.0-flash  # Optional, defaults to gemini-2.0-flash if GEMINI_API_KEY is set, otherwise gpt-3.5-turbo
```

## Installation

1. Install the required dependencies:
   ```bash
   pip install fastapi uvicorn python-dotenv
   ```

2. Make sure you have the existing RAG agent components installed (from requirements.txt)

## Running the API

### Development Mode

```bash
cd backend
python -m uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

### Using the Built-in Runner

```bash
cd backend
python api.py
```

The API will be available at `http://localhost:8000`

## API Endpoints

### GET /
- Health check endpoint
- Returns: `{"status": "ok", "message": "RAG Chatbot API is running"}`

### GET /health
- Detailed health check
- Returns system health status

### GET /system-info
- System configuration information
- Returns: collection name, model settings, etc.

### GET /validate-query
- Validates a query without processing it
- Query parameter: `question` (min length 3, max length 1000)
- Returns validation result

### POST /query
- Main endpoint for querying the RAG agent
- Request body:
  ```json
  {
    "question": "Your question here",
    "selected_text": "Optional selected text scope",
    "top_k": 5,
    "min_score": 0.3
  }
  ```
- Response includes content, sources, grounded status, and retrieved chunks

## Example Usage

```bash
# Query the RAG agent
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is ROS 2?",
    "top_k": 3,
    "min_score": 0.3
  }'
```

## Error Handling

- Invalid queries return 422 status code
- Processing errors return 500 status code with error details
- Rate limit errors are handled gracefully with fallback mechanisms

## Architecture

The API integrates with the existing RAG agent from `agent.py` and supports both OpenAI and Google's Gemini models through the OpenAI Agents SDK. The system automatically selects the appropriate model based on available API keys.