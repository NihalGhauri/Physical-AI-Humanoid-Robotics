# ADR-1: Frontend Chatbot UI Architecture for Docusaurus Integration

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together (e.g., "Frontend Stack" not separate ADRs for framework, styling, deployment).

- **Status:** Accepted
- **Date:** 2025-12-28
- **Feature:** 4-fastapi-integration
- **Context:** Need to implement a persistent chatbot UI that integrates with the Docusaurus book frontend to allow users to ask questions about book content and receive responses from the RAG agent.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security?
     2) Alternatives: Multiple viable options considered with tradeoffs?
     3) Scope: Cross-cutting concern (not an isolated detail)?
     If any are false, prefer capturing as a PHR note instead of an ADR. -->

## Decision

Implement a floating chatbot widget architecture that appears consistently across all pages of the Docusaurus book. The architecture includes:

- **Component Structure**:
  - ChatbotButton.tsx: Floating toggle button
  - ChatbotPanel.tsx: Main chat interface panel
  - MessageList.tsx: Displays conversation history
  - MessageInput.tsx: Input area for user questions
  - ChatbotStyles.module.css: Component-specific styles
  - api.ts: API client for backend communication

- **Integration Pattern**: Integrate directly into Docusaurus layout to appear on all pages
- **API Communication**: Use fetch API to communicate with FastAPI backend endpoints
- **State Management**: Maintain conversation history in component state with proper cleanup
- **User Experience**: Floating design with persistent access, source attribution display, and error handling

## Consequences

### Positive

- Consistent user experience across all book pages
- Persistent access to RAG functionality without navigation
- Clear source attribution for AI responses
- Proper error handling and fallback mechanisms
- Responsive design that works across device sizes
- Integration with existing Docusaurus theme

### Negative

- Additional complexity to page load times
- Potential layout conflicts with existing components
- Increased maintenance overhead for UI components
- Memory usage for maintaining chat session state
- Potential accessibility challenges if not properly implemented

## Alternatives Considered

Alternative A: Dedicated chat page instead of persistent widget
- Pros: Simpler implementation, isolated functionality
- Cons: Less convenient access, breaks user flow when reading content
- Rejected: Reduces usability and convenience

Alternative B: Inline chat integration within content pages
- Pros: Context-aware responses, natural integration with content
- Cons: Complex layout management, potential conflicts with existing content structure
- Rejected: Would require significant changes to existing page layouts

Alternative C: Browser extension approach
- Pros: Completely separate from website, reusable across sites
- Cons: Additional installation step for users, separate maintenance
- Rejected: Creates friction for users and increases complexity

## References

- Feature Spec: specs/4-fastapi-integration/spec.md
- Implementation Plan: specs/4-fastapi-integration/plan.md
- Related ADRs: None
- Evaluator Evidence: history/prompts/4-fastapi-integration/3-frontend-backend-integration-planning.plan.prompt.md