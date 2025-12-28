---
id: 2
title: Fix Coroutine Error in RAG Agent
stage: general
date: 2025-12-28
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: 1-rag-ingestion-pipeline
user: Claude Code
command: general
labels: ["backend", "error-fix", "async", "coroutine"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - E:\Final\Physical-AI-Humanoid-Robotics\backend\agent.py
tests: []
---

## User Prompt
```
start fast api server and website and read all logs and error and then fix errors and bugs
```

## Response
Identified and fixed the error `'coroutine' object has no attribute 'choices'` in the RAG agent.

### Problem
The error was occurring because the code was trying to access the `choices` attribute on a coroutine object instead of the actual response. This happened when using the async OpenAI client (for Gemini API) but calling it in a synchronous way.

### Changes Made

#### In `agent.py`:
1. Added `is_async_client` flag during initialization to track whether the client is async or sync
2. Updated `_generate_response_with_chat_completions` method to properly handle async clients:
   - Use asyncio event loop for async clients
   - Use synchronous calls for regular OpenAI clients
   - Properly await the async response before accessing its attributes
3. Used `asyncio.new_event_loop()` and `loop.run_until_complete()` to properly execute the async API call in a synchronous context

### Results
- Fixed the coroutine error that was preventing proper response generation
- Both sync (OpenAI) and async (Gemini) clients now work correctly
- FastAPI server starts without validation errors
- Docusaurus frontend is running on port 3000 and communicates properly with the backend