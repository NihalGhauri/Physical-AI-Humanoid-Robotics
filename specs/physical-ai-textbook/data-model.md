# Data Model: Physical AI & Humanoid Robotics Textbook

## Core Entities

### User
- `id` (UUID): Unique identifier
- `email` (string): User's email address
- `name` (string): User's full name
- `background` (string): Educational/professional background for personalization
- `preferences` (JSON): User preferences including language settings
- `created_at` (timestamp): Account creation time
- `updated_at` (timestamp): Last update time

### Module
- `id` (UUID): Unique identifier
- `title` (string): Module title (e.g. "Robotic Nervous System (ROS 2)")
- `description` (text): Module description
- `order` (integer): Display order in the curriculum
- `created_at` (timestamp): Creation time
- `updated_at` (timestamp): Last update time

### Chapter
- `id` (UUID): Unique identifier
- `module_id` (UUID): Reference to parent module
- `title` (string): Chapter title
- `content` (text): Chapter content in markdown format
- `order` (integer): Chapter order within the module
- `word_count` (integer): Number of words for reading time estimation
- `embeddings_status` (string): Status of embedding generation (pending, processing, completed)
- `created_at` (timestamp): Creation time
- `updated_at` (timestamp): Last update time

### Quiz
- `id` (UUID): Unique identifier
- `chapter_id` (UUID): Reference to the associated chapter
- `questions` (JSON): Array of quiz questions with options and answers
- `created_at` (timestamp): Creation time
- `updated_at` (timestamp): Last update time

### Summary
- `id` (UUID): Unique identifier
- `chapter_id` (UUID): Reference to the associated chapter
- `content` (text): Summary content
- `created_at` (timestamp): Creation time
- `updated_at` (timestamp): Last update time

### Translation
- `id` (UUID): Unique identifier
- `chapter_id` (UUID): Reference to the original chapter
- `language_code` (string): Language code (e.g. "ur" for Urdu)
- `content` (text): Translated content
- `created_at` (timestamp): Creation time
- `updated_at` (timestamp): Last update time

### Embedding
- `id` (UUID): Unique identifier
- `chapter_id` (UUID): Reference to the associated chapter
- `content_chunk` (text): Chunk of the chapter content that was embedded
- `vector` (array): Vector representation of the content chunk
- `chunk_index` (integer): Order of this chunk in the original content
- `created_at` (timestamp): Creation time

### APIUsage
- `id` (UUID): Unique identifier
- `user_id` (UUID): Reference to the user who made the request
- `endpoint` (string): The API endpoint that was called
- `request_data` (JSON): The request payload
- `response_data` (JSON): The response payload
- `tokens_used` (integer): Number of tokens used in the request
- `created_at` (timestamp): Request time

## Relationships
- User has many APIUsage records
- Module has many Chapters
- Chapter has one Summary
- Chapter has one Quiz
- Chapter has many Translations
- Chapter has many Embeddings