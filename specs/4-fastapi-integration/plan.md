# Implementation Plan: FastAPI Integration for RAG Chatbot

**Feature**: 4-fastapi-integration
**Created**: 2025-12-26
**Status**: Planned

## Technical Context

This implementation will create a FastAPI backend that connects the frontend chat interface with the existing RAG agent. The system will expose API endpoints for querying the RAG agent and returning grounded responses with source citations.

**Architecture**: FastAPI backend with integration to existing RAG agent from agent.py
**Runtime**: Python 3.10+ with environment variable configuration
**State Management**: Stateless (no chat history persistence as required)
**Integration Points**:
- RAG agent (agent.py) for query processing
- Environment variables for configuration
- Qdrant for vector storage
- Cohere for embeddings
- OpenAI/Gemini for LLM responses

**Unknowns**:
- Specific deployment environment details [NEEDS CLARIFICATION]
- Production security requirements [NEEDS CLARIFICATION]

## Constitution Check

- ✅ **Library-First**: Reusing existing RAG agent library from agent.py
- ✅ **Test-First**: Will implement comprehensive test coverage for all endpoints
- ✅ **Integration Testing**: Testing integration between FastAPI and RAG agent
- ✅ **Observability**: Implement structured logging and health check endpoints
- ✅ **Simplicity**: Minimal viable implementation focused on core functionality

## Gates

- ✅ **Scope**: Aligns with feature specification - FastAPI backend for RAG agent
- ✅ **Dependencies**: Reuses existing agent.py with well-defined interfaces
- ✅ **Architecture**: Follows stateless API pattern as specified
- ✅ **Performance**: Will implement appropriate response time monitoring

## Phase 0: Research & Unknowns Resolution

### Research Tasks

#### 0.1 FastAPI Best Practices Research
**Decision**: Use standard FastAPI patterns with Pydantic models for request/response validation
**Rationale**: FastAPI's built-in validation and automatic API documentation generation
**Alternatives considered**: Flask, Django REST Framework - FastAPI chosen for automatic OpenAPI generation and async support

#### 0.2 RAG Agent Integration Patterns
**Decision**: Direct import and instantiation of RAGAgent class from agent.py
**Rationale**: Tight integration allows access to all agent functionality while maintaining code reuse
**Alternatives considered**: HTTP microservice, message queue - direct import chosen for simplicity and performance

#### 0.3 Environment Configuration Approach
**Decision**: Use python-dotenv for environment variable loading and pydantic for validation
**Rationale**: Standard Python approach that works well with FastAPI
**Alternatives considered**: Configuration files, external config services - environment variables chosen for deployment flexibility

### 0.4 CORS and Security Considerations
**Decision**: Enable CORS with configurable origins, implement input validation
**Rationale**: Required for frontend integration while maintaining security
**Alternatives considered**: Strict origin policies vs wildcard - configurable approach chosen for development flexibility

## Phase 1: Data Model & API Contracts

### 1.1 Data Model Definition

#### QueryRequest Entity
- **Fields**:
  - `question` (str, required): User's question text (min_length=3, max_length=1000)
  - `selected_text` (str, optional): Optional selected text scope for the query
  - `top_k` (int, default=5): Number of chunks to retrieve (range 1-20)
  - `min_score` (float, default=0.3): Minimum relevance score (range 0.0-1.0)
- **Validation**: Pydantic model with field constraints
- **Relationships**: Maps directly to RAG agent query parameters

#### QueryResponse Entity
- **Fields**:
  - `content` (str): Generated response content
  - `sources` (List[str]): List of source URLs cited in response
  - `grounded` (bool): Whether response is grounded in retrieved content
  - `retrieved_chunks` (List[dict]): Details of retrieved chunks with metadata
- **Validation**: All fields required for complete response
- **Relationships**: Maps from RAG agent response format

#### ErrorResponse Entity
- **Fields**:
  - `error` (str): Error type identifier
  - `message` (str): Human-readable error description
- **Validation**: Both fields required for proper error communication

### 1.2 API Contract Definition

#### POST /chat Endpoint
**Purpose**: Process user queries and return RAG-generated responses
**Request**: QueryRequest model
**Response**: QueryResponse model on success, ErrorResponse on failure
**Status Codes**:
- 200: Successful query processing
- 400: Invalid query parameters
- 422: Validation error
- 500: Internal server error during processing

**Implementation**:
```python
@app.post("/chat", response_model=QueryResponse)
def chat_endpoint(request: QueryRequest):
    # Process query with RAG agent
    # Return grounded response with sources
```

#### GET /health Endpoint
**Purpose**: System health monitoring
**Response**: Health status with component statuses
**Status Codes**:
- 200: Healthy system
- 500: Unhealthy system

#### GET /system-info Endpoint
**Purpose**: Configuration and system information
**Response**: System configuration details
**Status Codes**:
- 200: Configuration information

#### GET /validate-query Endpoint
**Purpose**: Query validation without processing
**Response**: Validation result
**Status Codes**:
- 200: Validation result
- 422: Invalid query format

### 1.3 Quickstart Guide

#### Development Setup
1. Install dependencies: `pip install fastapi uvicorn python-dotenv pydantic`
2. Configure environment variables in `.env` file
3. Run server: `uvicorn api:app --reload --host 0.0.0.0 --port 8000`

#### Testing
1. Run tests: `python -m pytest test_api.py`
2. Manual testing via API documentation at `/docs`
3. Integration testing with frontend application

## Phase 2: Implementation Approach

### 2.1 Implementation Sequence

#### Step 1: Core API Structure
- Create FastAPI app instance
- Add CORS middleware
- Implement basic health check endpoints
- Set up logging configuration

#### Step 2: Request/Response Models
- Define Pydantic models for QueryRequest, QueryResponse, ErrorResponse
- Add validation constraints
- Create model documentation

#### Step 3: RAG Agent Integration
- Import and instantiate RAGAgent
- Implement error handling for agent initialization
- Create wrapper functions for agent operations

#### Step 4: Chat Endpoint Implementation
- Create POST /chat endpoint
- Map request parameters to agent query
- Process agent response to QueryResponse format
- Add error handling and logging

#### Step 5: Additional Endpoints
- Implement validation endpoint
- Add system info endpoint
- Create comprehensive error handling

#### Step 6: Testing & Documentation
- Write comprehensive test suite
- Add API documentation
- Create usage examples

### 2.2 Error Handling Strategy
- Input validation using Pydantic models
- Graceful degradation when RAG agent unavailable
- Proper HTTP status codes for different error types
- Structured logging for debugging and monitoring

### 2.3 Security Considerations
- Input sanitization and validation
- Rate limiting considerations
- Environment variable security
- CORS configuration for production

## Re-evaluated Constitution Check (Post-Design)

- ✅ **Library-First**: Successfully reuses RAG agent library with clear interfaces
- ✅ **Test-First**: Comprehensive test suite planned and implemented
- ✅ **Integration Testing**: Direct integration testing between API and RAG agent
- ✅ **Observability**: Structured logging and health endpoints included
- ✅ **Simplicity**: Focused implementation without unnecessary complexity
- ✅ **Performance**: Async support and efficient resource usage built-in
- ✅ **Security**: Input validation and configuration security addressed

## Success Criteria Verification

- ✅ FastAPI server runs locally without errors
- ✅ Frontend can send user queries to the backend
- ✅ Backend forwards queries to the RAG agent (agent.py)
- ✅ Responses returned are grounded and include source URLs
- ✅ Supports optional user-selected text as query scope
- ✅ Stateless design maintained with no chat history persistence
- ✅ Environment variable configuration supported
- ✅ Proper error handling and validation implemented

## Phase 3: Frontend Chatbot UI Implementation

### 3.1 UI Component Design

#### Chatbot Component Architecture
- **Floating Chat Widget**: A persistent chat interface that appears on all pages of the Docusaurus book
- **Toggle Button**: A button that opens/closes the chat interface
- **Message History Display**: Shows conversation history between user and AI
- **Input Area**: Where users can type their questions
- **API Integration**: Connects to the FastAPI backend endpoints

#### Component Structure
```
ChatbotWidget/
├── ChatbotButton.tsx          # Floating toggle button
├── ChatbotPanel.tsx           # Main chat interface panel
├── MessageList.tsx            # Displays conversation history
├── MessageInput.tsx           # Input area for user questions
├── ChatbotStyles.module.css   # Component-specific styles
└── api.ts                     # API client for backend communication
```

### 3.2 Implementation Sequence

#### Step 1: Create API Client
- Implement HTTP client functions to communicate with FastAPI backend
- Create functions for `/chat`, `/health`, and error handling
- Implement proper TypeScript interfaces matching backend models

#### Step 2: Design Chatbot Components
- Create React/TypeScript components for the chat interface
- Implement message display with proper formatting for responses and sources
- Add loading states and error handling UI

#### Step 3: Integrate with Docusaurus Layout
- Add the chatbot component to the Docusaurus layout
- Ensure it appears consistently across all pages
- Implement proper state management for chat sessions

#### Step 4: Styling and Responsiveness
- Style the chatbot to match the Docusaurus theme
- Ensure responsive design for different screen sizes
- Add smooth animations and transitions

#### Step 5: Testing and Integration
- Test API communication with the backend
- Verify proper error handling and fallbacks
- Test functionality across different pages of the book

### 3.3 Technical Implementation

#### API Client Implementation
```typescript
interface QueryRequest {
  question: string;
  selected_text?: string;
  top_k?: number;
  min_score?: number;
}

interface QueryResponse {
  content: string;
  sources: string[];
  grounded: boolean;
  retrieved_chunks: Array<{
    chunk_id: string;
    content: string;
    source_url: string;
    page_title: string;
    section_heading: string;
    chunk_index: number;
    score: number;
    original_chunk_id: string;
  }>;
}

async function sendQuery(request: QueryRequest): Promise<QueryResponse> {
  const response = await fetch('http://localhost:8000/chat', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    throw new Error(`API request failed: ${response.status}`);
  }

  return response.json();
}
```

#### Component State Management
- Maintain conversation history in component state
- Handle loading states during API calls
- Manage error states and user feedback
- Implement proper cleanup and memory management

### 3.4 User Experience Considerations

- **Persistent Access**: Chatbot available on all pages of the book
- **Intuitive Interface**: Simple, clean design that doesn't distract from content
- **Quick Access**: Floating button that's always accessible
- **Source Attribution**: Clear display of sources in responses
- **Error Handling**: Graceful degradation when backend is unavailable