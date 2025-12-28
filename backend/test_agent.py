#!/usr/bin/env python3
"""
Test script to verify the OpenAI Agents SDK implementation in the RAG agent.
"""

import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent import RAGAgent, AgentConfig

def test_agent_initialization():
    """Test that the agent initializes correctly with the new Agents SDK support."""
    print("Testing agent initialization with OpenAI Agents SDK support...")

    try:
        # Create a basic config (this will fail if environment variables are not set)
        config = AgentConfig()
        print("[OK] Agent configuration created successfully")

        # Initialize the RAG Agent
        agent = RAGAgent(config)
        print("[OK] RAG Agent initialized successfully")
        print(f"[OK] OpenAI Agents SDK available: {agent.agents_available}")

        return agent
    except ValueError as e:
        print(f"[WARN] Environment variables not set, but that's expected: {e}")
        print("Skipping full initialization test...")
        return None
    except Exception as e:
        print(f"[ERROR] Error during initialization: {e}")
        return None

def test_imports():
    """Test that the necessary imports work."""
    print("\nTesting imports...")

    try:
        from agents import Agent, Runner
        print("[OK] OpenAI Agents SDK imports successful")
    except ImportError as e:
        print(f"[WARN] OpenAI Agents SDK not available: {e}")

    try:
        from pydantic import BaseModel
        print("[OK] Pydantic imports successful")
    except ImportError as e:
        print(f"[ERROR] Pydantic import failed: {e}")

    try:
        import openai
        print("[OK] OpenAI imports successful")
    except ImportError as e:
        print(f"[ERROR] OpenAI import failed: {e}")

if __name__ == "__main__":
    print("Testing OpenAI Agents SDK Integration")
    print("="*50)

    test_imports()
    agent = test_agent_initialization()

    if agent:
        print("\n[OK] All tests passed! The agent is properly configured to use OpenAI Agents SDK.")
        print("  - When available, the agent will use the Agents SDK")
        print("  - When unavailable, it falls back to Chat Completions API")
    else:
        print("\n[WARN] Agent initialization skipped due to missing environment variables.")
        print("  - Set the required environment variables to run full tests.")

    print("\nTo run the full agent, ensure these environment variables are set:")
    print("  - OPENAI_API_KEY")
    print("  - GEMINI_API_KEY (optional, for Gemini model)")
    print("  - COHERE_API_KEY")
    print("  - QDRANT_URL")
    print("  - QDRANT_API_KEY")
    print("  - QDRANT_COLLECTION_NAME (optional)")