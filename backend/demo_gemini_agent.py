#!/usr/bin/env python3
"""
Demo script showing how to use the RAG Agent with Gemini API via OpenAI Agents SDK.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the backend directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent import RAGAgent, AgentConfig

def demo_gemini_agent():
    """Demonstrate the RAG Agent using Gemini API."""
    print("RAG Agent with Gemini API Demo")
    print("=" * 40)

    # Configure to use Gemini by setting the GEMINI_API_KEY in environment
    # If GEMINI_API_KEY is set, the agent will automatically use Gemini
    print(f"Gemini API Key available: {'Yes' if os.getenv('GEMINI_API_KEY') else 'No'}")
    print(f"OpenAI API Key available: {'Yes' if os.getenv('OPENAI_API_KEY') else 'No'}")
    print(f"Using model: {os.getenv('AGENT_MODEL_NAME', 'gemini-2.0-flash' if os.getenv('GEMINI_API_KEY') else 'gpt-3.5-turbo')}")

    try:
        # Initialize the agent (will use Gemini if GEMINI_API_KEY is set, otherwise OpenAI)
        agent = RAGAgent()
        print(f"\nAgent initialized successfully!")
        print(f"Agents SDK available: {agent.agents_available}")
        print(f"Using Gemini: {agent.config.use_gemini}")

        # Example query
        test_query = "What is ROS 2?"
        print(f"\nQuery: {test_query}")

        # Run a test query (this will use the retrieval system and then generate a response)
        print("Processing query...")
        response = agent.query(test_query, top_k=3)

        print(f"\nResponse: {response.content[:500]}...")  # Print first 500 chars
        print(f"Sources: {len(response.sources)} found")
        print(f"Grounded: {response.grounded}")

    except Exception as e:
        print(f"Error during demo: {e}")
        print("\nMake sure you have set the required environment variables:")
        print("- Either GEMINI_API_KEY or OPENAI_API_KEY")
        print("- COHERE_API_KEY")
        print("- QDRANT_URL")
        print("- QDRANT_API_KEY")


def demo_openai_agent():
    """Demonstrate the RAG Agent using OpenAI API."""
    print("\n" + "=" * 40)
    print("RAG Agent with OpenAI API Demo")
    print("=" * 40)

    # Temporarily unset GEMINI_API_KEY to force OpenAI usage (if it was set)
    original_gemini_key = os.environ.get('GEMINI_API_KEY')
    if original_gemini_key:
        del os.environ['GEMINI_API_KEY']

    try:
        # Initialize the agent with OpenAI
        agent = RAGAgent()
        print(f"Agent initialized successfully!")
        print(f"Agents SDK available: {agent.agents_available}")
        print(f"Using Gemini: {agent.config.use_gemini}")

        # Example query
        test_query = "What is humanoid robotics?"
        print(f"\nQuery: {test_query}")

        # Run a test query
        print("Processing query...")
        response = agent.query(test_query, top_k=3)

        print(f"\nResponse: {response.content[:500]}...")  # Print first 500 chars
        print(f"Sources: {len(response.sources)} found")
        print(f"Grounded: {response.grounded}")

    except Exception as e:
        print(f"Error during demo: {e}")
    finally:
        # Restore GEMINI_API_KEY if it was originally set
        if original_gemini_key:
            os.environ['GEMINI_API_KEY'] = original_gemini_key


if __name__ == "__main__":
    print("RAG Agent with OpenAI Agents SDK - Gemini/OpenAI Demo")
    print("=" * 60)

    # Run Gemini demo if GEMINI_API_KEY is available
    if os.getenv('GEMINI_API_KEY'):
        demo_gemini_agent()
    else:
        print("GEMINI_API_KEY not found. The agent will use OpenAI by default.")

    # Run OpenAI demo
    demo_openai_agent()

    print("\n" + "=" * 60)
    print("Demo completed!")