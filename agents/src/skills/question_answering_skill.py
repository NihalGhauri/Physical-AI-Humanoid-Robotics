"""
Question Answering Skill

Implements the core functionality for answering user questions about 
Physical AI & Humanoid Robotics textbook content using RAG.
"""
from typing import Dict, Any, List
from abc import ABC, abstractmethod


class QuestionAnsweringSkill(ABC):
    """Abstract interface for question answering functionality."""
    
    @abstractmethod
    def answer_question(self, query: str, user_id: str = None) -> Dict[str, Any]:
        """
        Answer a question based on textbook content.
        
        Args:
            query: The question to answer
            user_id: Optional user ID for personalization
            
        Returns:
            Dictionary containing the answer and citations
        """
        pass


class TextbookQASkill(QuestionAnsweringSkill):
    """Concrete implementation of question answering using RAG."""
    
    def __init__(self, rag_service):
        self.rag_service = rag_service
    
    def answer_question(self, query: str, user_id: str = None) -> Dict[str, Any]:
        """
        Answer a question using the RAG system with proper citations.
        
        Args:
            query: The question to answer
            user_id: Optional user ID for personalization
            
        Returns:
            Dictionary containing the answer, citations, and metadata
        """
        # Use the RAG service to find relevant textbook content
        response = self.rag_service.query(query, user_id)
        
        return {
            "answer": response["response"],
            "citations": response["citations"],
            "tokens_used": response.get("tokens_used", 0),
            "confidence": response.get("confidence", 0.0)
        }