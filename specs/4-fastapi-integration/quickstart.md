# Quickstart Guide: FastAPI Integration for RAG Chatbot

**Feature**: 4-fastapi-integration
**Date**: 2025-12-26

## Prerequisites

- Python 3.10 or higher
- pip package manager
- Access to API keys (OpenAI and/or Gemini, Cohere, Qdrant)

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Create Virtual Environment
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install fastapi uvicorn python-dotenv pydantic httpx
# Install other dependencies as specified in requirements.txt
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the `backend` directory:

```env
OPENAI_API_KEY=your_openai_api_key
GEMINI_API_KEY=your_gemini_api_key  # Optional
COHERE_API_KEY=your_cohere_api_key
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key
QDRANT_COLLECTION_NAME=Rag_Chatbot_book
AGENT_TEMPERATURE=0.7
AGENT_MAX_TOKENS=2048
AGENT_TOP_K=5
AGENT_MIN_SCORE=0.3
AGENT_MODEL_NAME=gemini-2.0-flash  # or gpt-3.5-turbo
```

## Running the Application

### Development Mode
```bash
cd backend
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode
```bash
cd backend
uvicorn api:app --host 0.0.0.0 --port 8000
```

### Using Built-in Runner
```bash
cd backend
python api.py
```

The API will be available at `http://localhost:8000`

## API Documentation
- Interactive API docs: `http://localhost:8000/docs`
- Alternative API docs: `http://localhost:8000/redoc`
- OpenAPI schema: `http://localhost:8000/openapi.json`

## Testing the API

### Example Query
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is the main purpose of this system?",
    "top_k": 3,
    "min_score": 0.3
  }'
```

### Example Query with Selected Text
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What does this text explain?",
    "selected_text": "ROS 2 is a set of software libraries and tools that help you build robot applications.",
    "top_k": 3,
    "min_score": 0.3
  }'
```

### Health Check
```bash
curl http://localhost:8000/health
```

## Key Endpoints

### POST /chat
- **Purpose**: Process user queries and return RAG-generated responses
- **Request Body**: QueryRequest object with question and optional parameters
- **Response**: QueryResponse object with grounded content and sources

### GET /health
- **Purpose**: Check system health status
- **Response**: Health status of all components

### GET /system-info
- **Purpose**: Get system configuration information
- **Response**: Configuration details including model settings

### GET /validate-query
- **Purpose**: Validate a query without processing it
- **Query Parameter**: question (required)
- **Response**: Validation result

## Troubleshooting

### Common Issues

1. **Environment Variables Not Loaded**
   - Ensure `.env` file is in the correct location
   - Verify all required environment variables are set

2. **RAG Agent Initialization Failure**
   - Check that all API keys are valid and have proper permissions
   - Verify Qdrant connection and collection exists

3. **API Request Timeouts**
   - Check network connectivity to external services (OpenAI, Cohere, Qdrant)
   - Verify API key quotas have not been exceeded

### Debugging
- Check application logs for error messages
- Use the health check endpoint to verify component status
- Review the API documentation for correct request formats

## Next Steps

1. Integrate with your frontend application
2. Configure production deployment settings
3. Set up monitoring and logging
4. Implement rate limiting if needed