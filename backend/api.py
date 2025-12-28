# #!/usr/bin/env python3
# """
# FastAPI backend for the RAG Chatbot
# Connects the frontend chat interface with the RAG agent, enabling users to ask questions about the book and receive grounded responses.
# """

# from fastapi import FastAPI, HTTPException, Query
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel, Field
# from typing import List, Optional
# import logging
# import os
# from dotenv import load_dotenv


# # Define Pydantic models for request/response
# class QueryRequest(BaseModel):
#     """Request model for querying the RAG agent"""
#     question: str = Field(..., min_length=3, max_length=1000, description="User's question text")
#     selected_text: Optional[str] = Field(None, description="Optional selected text scope for the query")
#     top_k: Optional[int] = Field(default=5, ge=1, le=20, description="Number of chunks to retrieve")
#     min_score: Optional[float] = Field(default=0.3, ge=0.0, le=1.0, description="Minimum relevance score")


# class QueryResponse(BaseModel):
#     """Response model from the RAG agent"""
#     content: str
#     sources: List[str]
#     grounded: bool
#     retrieved_chunks: List[dict]  # Using dict for simplicity, can be more specific if needed


# class ErrorResponse(BaseModel):
#     """Error response model"""
#     error: str
#     message: str

# # Load environment variables
# load_dotenv()

# # Import the RAG agent from the existing agent.py file
# from agent import RAGAgent, AgentConfig, AgentResponse

# # Configure logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# # Create FastAPI app
# app = FastAPI(
#     title="RAG Chatbot API",
#     description="API for the RAG Chatbot that connects frontend with RAG agent",
#     version="1.0.0"
# )

# # Add CORS middleware for frontend integration
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # In production, specify exact origins
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# # Initialize the RAG agent
# try:
#     agent = RAGAgent()
#     logger.info("RAG Agent initialized successfully")
# except Exception as e:
#     logger.error(f"Failed to initialize RAG Agent: {e}")
#     raise


# @app.get("/")
# def read_root():
#     """Health check endpoint"""
#     return {"status": "ok", "message": "RAG Chatbot API is running"}


# @app.get("/health")
# def health_check():
#     """Detailed health check endpoint"""
#     health_status = agent.health_check()
#     return health_status


# @app.post("/chat", response_model=QueryResponse, responses={400: {"model": ErrorResponse}})
# def chat_endpoint(request: QueryRequest):
#     """
#     Process a user query with the RAG agent and return a grounded response.

#     Args:
#         request: QueryRequest containing the question and optional parameters

#     Returns:
#         QueryResponse containing the answer with source citations
#     """
#     try:
#         logger.info(f"Processing query: {request.question[:50]}...")

#         # If selected text is provided, incorporate it into the query
#         question = request.question
#         if request.selected_text:
#             # Modify the question to focus on the selected text context
#             question = f"Regarding the selected text: '{request.selected_text}', {request.question}"

#         # Query the RAG agent
#         response: AgentResponse = agent.query(
#             question=question,
#             top_k=request.top_k,
#             min_score=request.min_score
#         )

#         # Convert the response to the expected format
#         result = QueryResponse(
#             content=response.content,
#             sources=response.sources,
#             grounded=response.grounded,
#             retrieved_chunks=[
#                 {
#                     "chunk_id": chunk.chunk_id,
#                     "content": chunk.content,
#                     "source_url": chunk.source_url,
#                     "page_title": chunk.page_title,
#                     "section_heading": chunk.section_heading,
#                     "chunk_index": chunk.chunk_index,
#                     "score": chunk.score,
#                     "original_chunk_id": chunk.original_chunk_id
#                 }
#                 for chunk in response.retrieved_chunks
#             ]
#         )

#         logger.info(f"Query processed successfully. Sources found: {len(response.sources)}")
#         return result

#     except ValueError as e:
#         logger.error(f"Invalid query: {e}")
#         raise HTTPException(status_code=400, detail=f"Invalid query: {str(e)}")
#     except Exception as e:
#         logger.error(f"Error processing query: {e}")
#         raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")


# @app.get("/validate-query")
# def validate_query_endpoint(question: str = Query(..., min_length=3, max_length=1000)):
#     """
#     Validate a query without processing it.

#     Args:
#         question: The question to validate

#     Returns:
#         Dictionary with validation result
#     """
#     try:
#         is_valid = agent.validate_query(question)
#         return {
#             "question": question,
#             "is_valid": is_valid,
#             "message": "Query is valid" if is_valid else "Query is invalid"
#         }
#     except Exception as e:
#         logger.error(f"Error validating query: {e}")
#         raise HTTPException(status_code=500, detail=f"Error validating query: {str(e)}")


# @app.get("/system-info")
# def system_info():
#     """
#     Get information about the system configuration.

#     Returns:
#         Dictionary with system configuration details
#     """
#     try:
#         return {
#             "collection_name": agent.config.collection_name,
#             "temperature": agent.config.temperature,
#             "max_tokens": agent.config.max_tokens,
#             "top_k": agent.config.top_k,
#             "min_score": agent.config.min_score,
#             "use_gemini": agent.config.use_gemini,
#             "model_name": agent.config.model_name,
#             "agents_sdk_available": agent.agents_available
#         }
#     except Exception as e:
#         logger.error(f"Error getting system info: {e}")
#         raise HTTPException(status_code=500, detail=f"Error getting system info: {str(e)}")


# if __name__ == "__main__":
#     import uvicorn
#     import os

#     # Get host and port from environment or use defaults
#     host = os.getenv("HOST", "0.0.0.0")
#     port = int(os.getenv("PORT", 8000))

#     logger.info(f"Starting server on {host}:{port}")

#     # Run the server
#     uvicorn.run(
#         "api:app",
#         host=host,
#         port=port,
#         reload=True,  # Enable auto-reload for development
#         log_level="info"
#     )


from dataclasses import dataclass
from typing import List
import logging

logger = logging.getLogger("agent")


@dataclass
class RetrievedChunk:
    chunk_id: str
    content: str
    source_url: str | None = None
    page_title: str | None = None
    section_heading: str | None = None
    chunk_index: int | None = None
    score: float | None = None
    original_chunk_id: str | None = None


@dataclass
class AgentResponse:
    content: str
    sources: List[str]
    grounded: bool
    retrieved_chunks: List[RetrievedChunk]


class AgentConfig:
    collection_name = "book"
    temperature = 0.2
    max_tokens = 1024
    top_k = 5
    min_score = 0.3
    model_name = "openrouter"
    use_gemini = False


class RAGAgent:
    def __init__(self):
        logger.info("Initializing TensorFlow-FREE RAG Agent")
        self.config = AgentConfig()
        self.agents_available = True

    def health_check(self):
        return {
            "status": "ok",
            "rag": "ready",
            "tensorflow": False,
        }

    def validate_query(self, question: str) -> bool:
        return isinstance(question, str) and len(question.strip()) >= 3

    def query(self, question: str, top_k: int, min_score: float) -> AgentResponse:
        """
        TEMP stub: replace with vector DB + LLM call
        """

        dummy_chunk = RetrievedChunk(
            chunk_id="demo-1",
            content="This is a placeholder answer until vector search is wired.",
            score=0.99,
        )

        return AgentResponse(
            content=f"Answer (stub): {question}",
            sources=["internal"],
            grounded=True,
            retrieved_chunks=[dummy_chunk],
        )
