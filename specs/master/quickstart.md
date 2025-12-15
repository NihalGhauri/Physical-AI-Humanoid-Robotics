# Quickstart Guide: Physical AI & Humanoid Robotics Textbook

## Development Setup

### Prerequisites
- Python 3.11
- Node.js 18+
- Git
- Access to free-tier services (Qdrant Cloud, Neon Postgres)

### Clone and Initialize
```bash
git clone <repository-url>
cd <repository-name>
```

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env  # Then update with your settings
python -m src.main  # To run the FastAPI server
```

### Website Setup
```bash
cd website
npm install
npm start  # To run the Docusaurus development server
```

### RAG Setup
```bash
cd rag
pip install -r requirements.txt
python -m src.embedding.generate_embeddings  # To generate initial embeddings
```

## Key Scripts

### Initialize textbook content
```bash
python -m src.textbook.load_content
```

### Generate embeddings for RAG
```bash
python -m src.rag.generate_embeddings
```

### Run tests
```bash
# Backend tests
cd backend && python -m pytest

# Website tests
cd website && npm test
```

### Build for production
```bash
# Backend
cd backend && python -m build

# Website
cd website && npm run build
```

## Configuration

### Environment Variables
- `NEON_DB_URL`: Connection string for Neon Postgres
- `QDRANT_URL`: Connection string for Qdrant Cloud
- `AUTH_SECRET`: Secret for Better-Auth
- `LLM_API_KEY`: API key for language model service
- `TRANSLATION_API_KEY`: API key for translation service

### API Endpoints
- `GET /api/textbook/modules`: List all textbook modules
- `GET /api/textbook/chapters/{module_id}`: List chapters for a module
- `GET /api/textbook/chapter/{chapter_id}`: Get specific chapter content
- `POST /api/query`: Submit a query to the RAG system
- `POST /api/auth/login`: User authentication
- `POST /api/translate`: Translate content to Urdu

## Testing the System

### Basic Functionality
1. Start the backend: `cd backend && python -m src.main`
2. Start the website: `cd website && npm start`
3. Visit the website and navigate through modules and chapters
4. Test the quiz and summary features
5. Try the Urdu translation toggle

### RAG Testing
1. Submit questions related to textbook content
2. Verify responses are cited and grounded in textbook material
3. Submit questions outside textbook scope and verify appropriate responses

### Authentication Testing
1. Create a user account
2. Log in and verify personalized content presentation
3. Test the personalization settings

## Troubleshooting

### Common Issues
- If embeddings aren't loading, check Qdrant connection and run the embedding generation script again
- If API calls are failing, verify environment variables are set correctly
- If translation isn't working, check the translation API key and service availability

### Performance
- For development, reduce embedding model size to speed up processing
- For production, consider caching frequently accessed content
- Monitor token usage to stay within free-tier limits