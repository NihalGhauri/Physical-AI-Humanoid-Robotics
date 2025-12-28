# Feature Specification: RAG Agent for Book Queries

**Feature Branch**: `1-rag-agent`
**Created**: 2025-12-26
**Status**: Draft
**Input**: User description: "RAG Agent Construction

What we're building:
A single RAG agent using the OpenAI Agents SDK that answers book-related questions by reasoning only over retrieved content from Qdrant.

Target audience:
Backend / AI engineers implementing agent-based RAG.

Focus:
Agent orchestration + retrieval tool integration + grounded answers.

Success criteria:
- Agent uses OpenAI Agents SDK
- Retrieval tool (from SPEC-2) is invoked for every book query
- Responses are grounded only in retrieved chunks
- Agent refuses to answer when no relevant context is found
- Source URLs are included in responses

Technical stack:
- OpenAI Agents SDK
- Python 3.10+
- Qdrant Cloud (existing vectors)
- Cohere embeddings (query embedding only)
- Environment variables via `.env`

Constraints:
- Must reuse SPEC-2 retrieval logic
- No direct LLM answers without retrieval
- Single agent (no multi-agent workflows)

Project structure:
- Use existing `backend/` folder
- Create one file: `agent.py`
- `agent.py` contains:
  - System instructions"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Query Books with Grounded Responses (Priority: P1)

As a backend/AI engineer, I want to ask book-related questions to a RAG agent so that I can get accurate answers based only on retrieved content from my knowledge base.

**Why this priority**: This is the core functionality of the RAG agent - providing grounded responses that only rely on retrieved content rather than hallucinating information.

**Independent Test**: The agent can accept a book-related question, retrieve relevant content from Qdrant, and respond with information that is directly grounded in the retrieved chunks with source URLs included.

**Acceptance Scenarios**:

1. **Given** a book-related question, **When** I submit it to the RAG agent, **Then** the agent retrieves relevant content from Qdrant and responds with information grounded only in that content with source URLs.
2. **Given** a book-related question with no relevant content in the knowledge base, **When** I submit it to the RAG agent, **Then** the agent refuses to answer and indicates that no relevant context was found.

---

### User Story 2 - Verify Grounded Responses (Priority: P1)

As a backend/AI engineer, I want to ensure that the agent's responses are always grounded in retrieved content so that I can trust the accuracy of the information provided.

**Why this priority**: This ensures the agent meets the core constraint of only providing answers based on retrieved content, not generating responses from its general knowledge.

**Independent Test**: The agent consistently refuses to answer questions when no relevant content is retrieved, and all provided answers include source URLs to the original content.

**Acceptance Scenarios**:

1. **Given** a question that requires information not present in the knowledge base, **When** I submit it to the RAG agent, **Then** the agent explicitly states it cannot answer due to lack of relevant context.
2. **Given** a valid question with relevant content in the knowledge base, **When** I submit it to the RAG agent, **Then** all information in the response is sourced from the retrieved chunks with proper attribution.

---

### User Story 3 - Integrate with Existing Retrieval Logic (Priority: P2)

As a backend/AI engineer, I want the RAG agent to reuse existing retrieval logic from SPEC-2 so that I can leverage proven retrieval mechanisms without duplicating effort.

**Why this priority**: Reusing existing retrieval logic ensures consistency and reduces development time while maintaining the reliability of the retrieval process.

**Independent Test**: The RAG agent successfully invokes the SPEC-2 retrieval tool for every book query and receives relevant content from Qdrant.

**Acceptance Scenarios**:

1. **Given** a book-related question, **When** I submit it to the RAG agent, **Then** the agent invokes the SPEC-2 retrieval tool and receives relevant content chunks from Qdrant.

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST use OpenAI Agents SDK to implement the RAG agent
- **FR-002**: System MUST invoke the retrieval tool from SPEC-2 for every book query
- **FR-003**: System MUST ensure all responses are grounded only in retrieved content chunks from Qdrant
- **FR-004**: System MUST refuse to answer when no relevant context is found in the knowledge base
- **FR-005**: System MUST include source URLs in all responses that reference the original content
- **FR-006**: System MUST reuse the SPEC-2 retrieval logic without duplicating functionality
- **FR-007**: System MUST NOT provide direct LLM answers without retrieval of relevant content
- **FR-008**: System MUST implement as a single agent without multi-agent workflows
- **FR-009**: System MUST use Cohere embeddings for query embedding only
- **FR-010**: System MUST store configuration in environment variables via `.env` file

### Key Entities *(include if feature involves data)*

- **RAG Agent**: The AI agent that processes book-related questions and responds based only on retrieved content
- **Retrieval Tool**: The component that connects to Qdrant Cloud to fetch relevant content chunks based on the query
- **Query**: A book-related question submitted by the user that requires grounded responses
- **Retrieved Content**: Chunks of text retrieved from Qdrant that contain relevant information to answer the query
- **Response**: The agent's answer that is grounded only in retrieved content with source attribution

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of agent responses are grounded only in retrieved content chunks from Qdrant with proper source attribution
- **SC-002**: Agent refuses to answer at least 95% of queries when no relevant context is found in the knowledge base
- **SC-003**: All responses include source URLs that reference the original content from which information was derived
- **SC-004**: Agent successfully integrates with SPEC-2 retrieval logic without reimplementing existing functionality
- **SC-005**: Agent achieves 90% accuracy in providing answers that are factually consistent with retrieved content