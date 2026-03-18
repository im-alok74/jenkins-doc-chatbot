export interface ChatContext {
  job_name?: string;
  build_id?: string;
  console_log?: string;
  build_status?: 'Success' | 'Failed' | 'Running';
}

export interface ConversationTurn {
  role: 'user' | 'assistant';
  content: string;
}

export interface ChatRequest {
  query: string;
  context?: ChatContext;
  conversation_history: ConversationTurn[];
}

export interface ChatResponse {
  response: string;
  sources: string[];
  confidence: number;
}

export interface LogAnalysisRequest {
  console_log: string;
  job_name?: string;
}

export interface LogAnalysisResponse {
  error_type: string;
  summary: string;
  root_cause: string;
  fix_suggestions: string[];
  relevant_stage: string;
}

export interface DocSearchResult {
  content: string;
  source: string;
  relevance_score: number;
}

export interface DocSearchResponse {
  results: DocSearchResult[];
}

export interface HealthResponse {
  status: string;
  version: string;
}
