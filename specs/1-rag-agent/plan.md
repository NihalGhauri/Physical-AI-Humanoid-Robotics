# Implementation Plan: RAG Agent for Book Queries

**Feature**: 1-rag-agent
**Created**: 2025-12-26
**Status**: Draft
**Input**: Spec -3: Agent with Retrieval - Create `backend/agent.py`, Initialize OpenAI Agent SDK with system instructions, integrate retrieval by calling the existing Qdrant search logic, Implement retrieval logic (top-k similarity search) in `agent.py`, Execute agent with retrieval-grounded responses

## Technical Context

This plan outlines the implementation of a RAG (Retrieval-Augmented Generation) agent that uses OpenAI's Agent SDK to answer book-related questions. The agent will integrate with Qdrant for vector search and Cohere for embeddings, ensuring responses are grounded only in retrieved content with proper source attribution.

### Architecture Overview

- **Agent Core**: OpenAI Agent SDK implementation in `backend/agent.py`
- **Retrieval Component**: Integration with existing Qdrant search logic
- **Embedding Service**: Cohere for converting queries to embeddings
- **Response Handler**: Logic to ensure responses are grounded in retrieved content

### Dependencies

- OpenAI Python SDK
- Cohere Python SDK
- Qdrant Python client
- Python 3.10+
- Environment configuration via `.env`

### Unknowns

- Specific system instructions for the agent (NEEDS CLARIFICATION)

## Constitution Check

Based on the project constitution principles:

- **Test-First**: All components will be developed with TDD approach
- **Observability**: Proper logging will be implemented for debugging and monitoring
- **Simplicity**: Starting with minimal viable implementation and adding complexity only as needed

### Compliance Verification

- [ ] All code will follow test-first methodology
- [ ] Proper error handling and logging will be implemented
- [ ] Code will be modular and maintainable
- [ ] Security best practices for API keys and environment variables will be followed

## Phase 0: Research & Unknown Resolution

### Research Tasks

1. **System Instructions Definition**
   - Task: Define the system instructions that will guide the agent's behavior
   - Goal: Create instructions that ensure responses are grounded only in retrieved content

2. **OpenAI Agent SDK Implementation**
   - Task: Research best practices for OpenAI Agent SDK implementation
   - Goal: Determine optimal approach for agent initialization and execution

### Resolved Research

1. **SPEC-2 Retrieval Logic Location**
   - Resolved: Located in `backend/retrieve.py` - the `RetrievalValidator.retrieve_chunks()` method
   - Integration: Will reuse the existing retrieval logic that performs top-k similarity search

2. **Qdrant Integration Details**
   - Resolved: Collection uses 1024-dim vectors with cosine distance, collection name from env var
   - Schema: Payload includes content, source_url, page_title, section_heading, chunk_index, original_chunk_id

3. **Cohere Embeddings Integration**
   - Resolved: Uses "embed-english-v3.0" model with "search_query" input type for queries
   - Method: Query embeddings are generated using the Cohere embed API

## Phase 1: Design & Architecture

### Data Model

Completed and documented in `data-model.md`

### API Contracts

Completed and documented in `contracts/rag-agent-api.yaml`

### System Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   User Query    │───▶│  Agent Service   │───▶│  OpenAI Agent   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │  Retrieval Logic │
                       │ (retrieve.py)    │
                       └──────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │  Embedding API   │
                       │ (Cohere)         │
                       └──────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │   Qdrant DB      │
                       └──────────────────┘
```

### Integration Points

- **Retrieval Integration**: Reuse `RetrievalValidator.retrieve_chunks()` from `backend/retrieve.py`
- **Embedding Integration**: Use Cohere's embed API with "embed-english-v3.0" model
- **Qdrant Integration**: Use existing configuration from environment variables
- **OpenAI Agent**: Initialize with system instructions that enforce grounded responses

## Phase 2: Implementation Approach

### Step 1: Environment Setup
- Create `.env` file with API keys
- Set up Python virtual environment
- Install required dependencies

### Step 2: Core Agent Implementation
- Create `backend/agent.py`
- Initialize OpenAI Agent SDK
- Implement basic agent functionality

### Step 3: Retrieval Integration
- Integrate with SPEC-2 retrieval logic
- Implement top-k similarity search
- Handle query embedding with Cohere

### Step 4: Grounded Response Logic
- Implement logic to ensure responses are based only on retrieved content
- Add source URL attribution
- Implement refusal when no relevant context is found

### Step 5: Testing and Validation
- Write unit tests for each component
- Create integration tests
- Validate all functional requirements