/**
 * API client for communicating with the FastAPI backend
 * Handles all communication with the RAG agent backend
 */

interface QueryRequest {
  question: string;
  selected_text?: string;
  top_k?: number;
  min_score?: number;
}

interface RetrievedChunk {
  chunk_id: string;
  content: string;
  source_url: string;
  page_title: string;
  section_heading: string;
  chunk_index: number;
  score: number;
  original_chunk_id: string;
}

interface QueryResponse {
  content: string;
  sources: string[];
  grounded: boolean;
  retrieved_chunks: RetrievedChunk[];
}

interface ErrorResponse {
  error: string;
  message: string;
}

/**
 * Sends a query to the backend RAG agent
 * @param request - The query request with question and optional parameters
 * @param signal - AbortSignal to handle request cancellation
 * @returns Promise resolving to QueryResponse
 * @throws Error if the API request fails
 */
export async function sendQuery(request: QueryRequest, signal?: AbortSignal): Promise<QueryResponse> {
  try {
    const response = await fetch('http://localhost:8000/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
      signal, // Add signal for request cancellation
    });

    if (!response.ok) {
      if (response.status === 422) {
        // Handle 422 status specifically
        throw new Error('API request failed: 422');
      }
      const errorData: ErrorResponse = await response.json().catch(() => ({}));
      throw new Error(errorData.message || `API request failed: ${response.status}`);
    }

    const data: QueryResponse = await response.json();
    return data;
  } catch (error) {
    if (error instanceof DOMException && (error.name === 'AbortError' || error.name === 'TimeoutError')) {
      // Handle request cancellation/interruption
      throw new Error('Request interrupted by user');
    }
    if (error instanceof TypeError && error.message.includes('fetch')) {
      // Network error (backend unavailable)
      throw new Error('Network error: Unable to connect to the backend service. Please check your connection and try again later.');
    }
    if (error instanceof Error) {
      throw error;
    }
    throw new Error('Unknown error occurred while sending query');
  }
}

/**
 * Sends a query to the backend RAG agent with retry logic
 * @param request - The query request with question and optional parameters
 * @param maxRetries - Maximum number of retry attempts (default: 3)
 * @param signal - AbortSignal to handle request cancellation
 * @returns Promise resolving to QueryResponse
 * @throws Error if the API request fails after all retries
 */
export async function sendQueryWithRetry(request: QueryRequest, maxRetries: number = 3, signal?: AbortSignal): Promise<QueryResponse> {
  let lastError: Error | null = null;

  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await sendQuery(request, signal);
    } catch (error) {
      lastError = error as Error;

      // If this was the last attempt, throw the error
      if (attempt === maxRetries) {
        break;
      }

      // Check if request was cancelled during retry
      if (signal?.aborted) {
        throw new Error('Request interrupted by user');
      }

      // Wait before retrying (exponential backoff)
      await new Promise(resolve => setTimeout(resolve, Math.pow(2, attempt) * 1000));
    }
  }

  throw lastError;
}

/**
 * Checks the health status of the backend service
 * @returns Promise resolving to health status
 */
export async function checkHealth(): Promise<any> {
  try {
    const response = await fetch('http://localhost:8000/health', {
      method: 'GET',
    });

    if (!response.ok) {
      throw new Error(`Health check failed: ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    if (error instanceof Error) {
      throw error;
    }
    throw new Error('Unknown error occurred during health check');
  }
}

/**
 * Validates a query without processing it
 * @param question - The question to validate
 * @returns Promise resolving to validation result
 */
export async function validateQuery(question: string): Promise<{ question: string; is_valid: boolean; message: string }> {
  try {
    const response = await fetch(`http://localhost:8000/validate-query?question=${encodeURIComponent(question)}`, {
      method: 'GET',
    });

    if (!response.ok) {
      throw new Error(`Query validation failed: ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    if (error instanceof Error) {
      throw error;
    }
    throw new Error('Unknown error occurred during query validation');
  }
}