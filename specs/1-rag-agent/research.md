# Research Findings: RAG Agent Implementation

## Decision: SPEC-2 Retrieval Logic Location
**Rationale**: Need to locate the existing retrieval logic from SPEC-2 to reuse it in the agent implementation
**Investigation**: Found existing retrieval implementation in `backend/retrieve.py`
**Action**: Use the `RetrievalValidator` class which contains the retrieval logic with `retrieve_chunks` method that performs top-k similarity search in Qdrant

## Decision: Qdrant Collection Structure
**Rationale**: Need to understand the schema and structure of the Qdrant collection to perform proper similarity search
**Investigation**: From `backend/retrieve.py` and `backend/vector_storage.py`, the collection has:
- Collection name: `Rag_Chatbot_book` (from environment variable)
- Vector size: 1024 dimensions (Cohere v3.0 embeddings)
- Payload structure includes: content, source_url, page_title, section_heading, chunk_index, original_chunk_id
- Uses cosine distance for similarity search
**Action**: Use existing collection structure and schema

## Decision: OpenAI Agent SDK Configuration
**Rationale**: Need to determine the best way to initialize and configure the OpenAI Agent SDK for our use case
**Investigation**: Will use OpenAI's Agent SDK to create an agent that integrates with the existing retrieval logic
**Action**: Initialize OpenAI Agent SDK and create system instructions that enforce grounded responses

## Decision: System Instructions Content
**Rationale**: Need to define the system instructions that will guide the agent's behavior
**Investigation**: System instructions should ensure responses are grounded only in retrieved content and include source attribution
**Action**: Create system instructions that:
- Only respond based on retrieved content from Qdrant
- Include source URLs in responses
- Refuse to answer when no relevant context is found
- Follow proper grounding principles

## Decision: Cohere API Configuration
**Rationale**: Need to understand how to properly integrate with Cohere for query embeddings
**Investigation**: From `backend/retrieve.py`, Cohere is used with:
- Model: "embed-english-v3.0"
- Input type: "search_query" for queries
- Query embeddings are generated using the embed API
**Action**: Use existing Cohere configuration for query embedding

## Resolved Unknowns
1. **SPEC-2 Retrieval Logic**: Located in `backend/retrieve.py` - the `RetrievalValidator.retrieve_chunks()` method
2. **Qdrant Collection Structure**: Uses 1024-dim vectors with cosine distance, collection name from env var
3. **Cohere Configuration**: Uses "embed-english-v3.0" model with "search_query" input type
4. **System Instructions**: Will be defined to enforce grounded responses with source attribution

## Next Steps
1. Create `backend/agent.py` with OpenAI Agent SDK integration
2. Integrate with existing retrieval logic from `backend/retrieve.py`
3. Implement system instructions that enforce grounded responses
4. Ensure proper source URL attribution in responses