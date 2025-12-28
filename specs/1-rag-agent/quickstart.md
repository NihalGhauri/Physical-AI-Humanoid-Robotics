# Quickstart Guide: RAG Agent for Book Queries

## Prerequisites

- Python 3.10+
- OpenAI API key
- Cohere API key
- Qdrant Cloud account and API key
- Git

## Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install openai cohere qdrant-client python-dotenv
```

### 4. Configure Environment Variables
Create a `.env` file in the project root with the following:

```env
OPENAI_API_KEY=your_openai_api_key_here
COHERE_API_KEY=your_cohere_api_key_here
QDRANT_URL=your_qdrant_cloud_url_here
QDRANT_API_KEY=your_qdrant_api_key_here
QDRANT_COLLECTION_NAME=Rag_Chatbot_book
```

## Usage

### 1. Initialize the RAG Agent
```python
from backend.agent import RAGAgent

# Initialize the agent
agent = RAGAgent()
```

### 2. Query the Agent
```python
# Ask a book-related question
question = "What are the key principles of humanoid robotics?"
response = agent.query(question, top_k=5)

print(f"Response: {response['content']}")
print(f"Sources: {response['sources']}")
print(f"Grounded: {response['grounded']}")
```

### 3. Validate Retrieval System
```python
# Validate that the retrieval system is working
is_valid = agent.validate_retrieval()
print(f"Retrieval system valid: {is_valid}")
```

## Testing

### Run Basic Functionality Test
```bash
python -c "
from backend.agent import RAGAgent
agent = RAGAgent()
result = agent.query('What is ROS 2?')
print('Test query result:', result)
"
```

### Run Comprehensive Validation
```bash
python backend/retrieve.py  # This runs the existing validation
```

## Troubleshooting

### Common Issues

1. **API Keys Not Found**
   - Ensure all required environment variables are set
   - Check that `.env` file is in the correct location

2. **Qdrant Connection Issues**
   - Verify QDRANT_URL and QDRANT_API_KEY are correct
   - Ensure the collection name matches what was used during ingestion

3. **No Results for Queries**
   - Verify that documents have been ingested into Qdrant
   - Check that the collection contains relevant content

4. **Embedding Generation Issues**
   - Ensure Cohere API key is valid and has sufficient quota
   - Check that the Cohere service is accessible

## Next Steps

1. Integrate the agent into your application
2. Customize the system instructions for your specific use case
3. Monitor agent performance and adjust retrieval parameters as needed
4. Add error handling and logging for production use