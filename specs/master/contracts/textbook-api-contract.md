# Textbook Content API Contract

## Module Endpoints

### GET /api/modules
**Description**: Retrieve all textbook modules

**Response**:
```json
{
  "modules": [
    {
      "id": "uuid",
      "title": "string",
      "description": "string",
      "order": "integer"
    }
  ]
}
```

### GET /api/modules/{module_id}/chapters
**Description**: Retrieve all chapters for a specific module

**Parameters**:
- `module_id` (path): The ID of the module

**Response**:
```json
{
  "chapters": [
    {
      "id": "uuid",
      "title": "string",
      "module_id": "uuid",
      "order": "integer",
      "word_count": "integer"
    }
  ]
}
```

### GET /api/chapters/{chapter_id}
**Description**: Retrieve specific chapter content

**Parameters**:
- `chapter_id` (path): The ID of the chapter

**Response**:
```json
{
  "id": "uuid",
  "title": "string",
  "content": "string",
  "module_id": "uuid",
  "order": "integer",
  "word_count": "integer",
  "embeddings_status": "string"
}
```

## Authentication Endpoints

### POST /api/auth/register
**Description**: Register a new user

**Request**:
```json
{
  "email": "string",
  "name": "string",
  "password": "string"
}
```

**Response**:
```json
{
  "user_id": "uuid",
  "email": "string",
  "name": "string"
}
```

### POST /api/auth/login
**Description**: Authenticate user and return session token

**Request**:
```json
{
  "email": "string",
  "password": "string"
}
```

**Response**:
```json
{
  "token": "string",
  "user": {
    "id": "uuid",
    "email": "string",
    "name": "string"
  }
}
```

## RAG Endpoints

### POST /api/query
**Description**: Submit a query to the RAG system and get a response with citations

**Headers**:
- `Authorization`: Bearer token

**Request**:
```json
{
  "query": "string",
  "user_id": "uuid"
}
```

**Response**:
```json
{
  "response": "string",
  "citations": [
    {
      "chapter_id": "uuid",
      "chapter_title": "string",
      "url": "string"
    }
  ],
  "tokens_used": "integer"
}
```

## User Preferences Endpoints

### GET /api/users/{user_id}/preferences
**Description**: Get user preferences including personalization settings

**Response**:
```json
{
  "background": "string",
  "preferences": {
    "language": "string",
    "content_level": "string"
  }
}
```

### PUT /api/users/{user_id}/preferences
**Description**: Update user preferences

**Request**:
```json
{
  "background": "string",
  "preferences": {
    "language": "string",
    "content_level": "string"
  }
}
```

**Response**:
```json
{
  "message": "string"
}
```

## Translation Endpoints

### POST /api/translate
**Description**: Translate chapter content to Urdu

**Request**:
```json
{
  "chapter_id": "uuid",
  "target_language": "string"
}
```

**Response**:
```json
{
  "translated_content": "string"
}
```

## Summary and Quiz Endpoints

### GET /api/chapters/{chapter_id}/summary
**Description**: Retrieve auto-generated summary for a chapter

**Response**:
```json
{
  "summary": "string"
}
```

### GET /api/chapters/{chapter_id}/quiz
**Description**: Retrieve auto-generated quiz for a chapter

**Response**:
```json
{
  "questions": [
    {
      "id": "uuid",
      "question": "string",
      "options": ["string"],
      "correct_answer": "string"
    }
  ]
}
```