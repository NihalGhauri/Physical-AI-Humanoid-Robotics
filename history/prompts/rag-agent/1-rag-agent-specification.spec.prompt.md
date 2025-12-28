---
id: 1
title: rag-agent-specification
stage: spec
date: 2025-12-26
surface: agent
model: claude-sonnet-4-5-20250929
feature: rag-agent
branch: 1-rag-agent
user: Claude Code User
command: /sp.specify RAG Agent Construction
labels: ["spec", "rag", "agent", "openai"]
links:
  spec: specs/1-rag-agent/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/1-rag-agent/spec.md
 - specs/1-rag-agent/checklists/requirements.md
tests:
 -
---

## Prompt

RAG Agent Construction

What we're building:
A single RAG agent using the OpenAI Agents SDK that answers book-related questions by reasoning only over retrieved content from Qdrant.

Target audience:
Backend / AI engineers implementing agent-based RAG.

Focus:
Agent orchestration + retrieval tool integration + grounded answers.

Success criteria:
- Agent uses OpenAI Agents SDK
- Retrieval tool (from SPEC-2) is invoked for every book query
- Responses are grounded only in retrieved chunks
- Agent refuses to answer when no relevant context is found
- Source URLs are included in responses

Technical stack:
- OpenAI Agents SDK
- Python 3.10+
- Qdrant Cloud (existing vectors)
- Cohere embeddings (query embedding only)
- Environment variables via `.env`

Constraints:
- Must reuse SPEC-2 retrieval logic
- No direct LLM answers without retrieval
- Single agent (no multi-agent workflows)

Project structure:
- Use existing `backend/` folder
- Create one file: `agent.py`
- `agent.py` contains:
  - System instructions

## Response snapshot

Created a comprehensive specification for the RAG Agent Construction feature, including user scenarios, functional requirements, and success criteria. The specification captures the core requirements of using OpenAI Agents SDK, ensuring responses are grounded only in retrieved content, and including source URLs in responses.

## Outcome

- ✅ Impact: Created complete feature specification for RAG agent that answers book-related questions with grounded responses
- 🧪 Tests: N/A (specification work)
- 📁 Files: Created spec.md and requirements checklist for the RAG agent feature
- 🔁 Next prompts: Ready for /sp.clarify or /sp.plan to continue development
- 🧠 Reflection: Successfully created a detailed spec that captures all requirements from the user description

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed with planning phase