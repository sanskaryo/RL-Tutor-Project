/**
 * API Client for RL Educational Tutor Backend
 * Base URL configured via environment variables
 */

import {
  ProgressResponse,
  RLStats,
  PerformancePoint,
  LearningStyleQuiz,
  LearningStyleAnswers,
  LearningStyleResult
} from './types';

/**
 * Get auth token from local storage
 */
export const getAuthToken = () => {
  if (typeof window !== 'undefined') {
    return localStorage.getItem('token');
  }
  return null;
};

/**
 * Clear auth token from local storage
 */
export const clearAuthToken = () => {
  if (typeof window !== 'undefined') {
    localStorage.removeItem('token');
  }
};

/**
 * Get auth headers
 */
export const getAuthHeaders = () => {
  const token = getAuthToken();
  return {
    'Content-Type': 'application/json',
    ...(token ? { 'Authorization': `Bearer ${token}` } : {})
  };
};

// Ensure no trailing slash in the base URL
const API_BASE = (process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8002/api/v1').replace(/\/+$/, '');

// ==================== TYPES ====================
export interface RegisterData {
    email: string;
    username: string;
    password: string;
    full_name?: string;
}

export interface LoginData {
    username: string;
    password: string;
}

export interface TokenResponse {
    access_token: string;
    token_type: string;
}

export interface Student {
    id: number;
    email: string;
    username: string;
    full_name: string | null;
    created_at: string;
}

export interface Content {
    id: number;
    title: string;
    description: string | null;
    topic: string;
    difficulty: number;
    content_type: string;
    question_text: string;
    options: string[] | null;
}

export interface AnswerData {
    session_id: number;
    student_answer: string;
    time_spent: number;
}

export interface SessionResponse {
    id: number;
    content_id: number;
    is_correct: boolean;
    reward: number;
    explanation: string;
    next_content: Content | null;
}

export interface KnowledgeState {
    algebra_score: number;
    calculus_score: number;
    geometry_score: number;
    statistics_score: number;
    accuracy_rate: number;
    preferred_difficulty: number;
    learning_style: string;
}

export interface ProgressData {
    total_attempts: number;
    correct_answers: number;
    accuracy_rate: number;
    topics_mastered: string[];
    current_streak: number;
    time_spent_today: number;
    skill_improvements: Record<string, number>;
}

export interface SessionSummary {
    id: number;
    content_id: number;
    is_correct: boolean;
    reward: number;
    created_at: string;
    topic: string;
}

export interface DashboardData {
    student: Student;
    knowledge: KnowledgeState;
    progress: ProgressData;
    recent_sessions: SessionSummary[];
}

export interface RecommendedContent {
    id: number;
    title: string;
    topic: string;
    difficulty: number;
    confidence: number;
    reason: string;
}

export interface KnowledgeGap {
    topic: string;
    score: number;
    recommendation: string;
}

export interface LearningStyleInfo {
    style: string;
    visual_score: number;
    auditory_score: number;
    reading_score: number;
    kinesthetic_score: number;
}

export interface DashboardRecommendations {
    learning_style: LearningStyleInfo;
    recommended_content: RecommendedContent[];
    study_tips: string[];
    knowledge_gaps: KnowledgeGap[];
    next_action: string;
}

// ==================== API CLIENT ====================
class ApiClient {
    private baseUrl: string;

    constructor(baseUrl: string) {
        this.baseUrl = baseUrl;
    }

    // Helper method for fetch requests
    private async request<T>(
        endpoint: string,
        options: RequestInit = {}
    ): Promise<T> {
        const url = `${this.baseUrl}${endpoint}`;
        
        console.log(`[API] ${options.method || 'GET'} ${url}`);

        const response = await fetch(url, {
            ...options,
            headers: {
                ...getAuthHeaders(),
                ...options.headers,
            },
        });

        console.log(`[API] Response ${response.status} from ${endpoint}`);

        if (!response.ok) {
            let error;
            const contentType = response.headers.get('content-type');
            
            if (contentType && contentType.includes('application/json')) {
                error = await response.json().catch(() => ({ detail: 'Failed to parse error response' }));
            } else {
                const text = await response.text().catch(() => '');
                error = { detail: text || `HTTP ${response.status}` };
            }
            
            console.error(`[API] Error (${response.status}):`, error);
            
            // Handle specific error cases
            if (response.status === 401) {
                console.error('[API] Unauthorized - Token may be invalid or expired');
            }
            
            throw new Error(error.detail || error.error || `HTTP ${response.status}`);
        }

        return response.json();
    }

    // ==================== AUTH ENDPOINTS ====================
    async register(data: RegisterData): Promise<TokenResponse> {
        return this.request<TokenResponse>('/auth/register', {
            method: 'POST',
            body: JSON.stringify(data),
        });
    }

    async login(data: LoginData): Promise<TokenResponse> {
        const response = await this.request<TokenResponse>('/auth/login', {
            method: 'POST',
            body: JSON.stringify(data),
        });
        
        // Store the token in localStorage
        if (typeof window !== 'undefined' && response.access_token) {
            localStorage.setItem('token', response.access_token);
        }
        
        return response;
    }

    async logout(): Promise<void> {
        clearAuthToken();
    }

    async getProfile(token: string): Promise<Student> {
        return this.request<Student>(`/auth/me?token=${token}`);
    }

    // ==================== SESSION ENDPOINTS ====================
    async startSession(
        username: string,
        topic?: string,
        difficulty?: number
    ): Promise<Content> {
        const params = new URLSearchParams({ username });
        const body: { topic?: string; difficulty?: number } = {};
        if (topic) body.topic = topic;
        if (difficulty) body.difficulty = difficulty;

        return this.request<Content>(`/session/start?${params}`, {
            method: 'POST',
            body: JSON.stringify(body),
        });
    }

    async submitAnswer(username: string, data: AnswerData): Promise<SessionResponse> {
        const params = new URLSearchParams({ username });
        return this.request<SessionResponse>(`/session/answer?${params}`, {
            method: 'POST',
            body: JSON.stringify(data),
        });
    }

    async getProgress(username: string): Promise<ProgressResponse> {
        const params = new URLSearchParams({ username });
        return this.request<ProgressResponse>(`/session/progress?${params}`);
    }

    // ==================== ANALYTICS ENDPOINTS ====================
    async getDashboard(username: string): Promise<DashboardData> {
        const params = new URLSearchParams({ username });
        return this.request<DashboardData>(`/analytics/dashboard?${params}`);
    }

    async getRLStats(): Promise<RLStats> {
        return this.request<RLStats>('/analytics/rl-stats');
    }

    async getPerformanceChart(username: string, days: number = 7): Promise<PerformancePoint[]> {
        const params = new URLSearchParams({
            username,
            days: days.toString()
        });
        return this.request<PerformancePoint[]>(`/analytics/performance-chart?${params}`);
    }

    // ==================== RECOMMENDATIONS ENDPOINTS ====================
    async getDashboardRecommendations(): Promise<DashboardRecommendations> {
        return this.request<DashboardRecommendations>('/recommendations/dashboard');
    }

    // ==================== LEARNING STYLE ENDPOINTS ====================
    async getLearningStyleQuiz(): Promise<LearningStyleQuiz> {
        return this.request<LearningStyleQuiz>('/quiz');
    }

    async submitLearningStyle(userId: string, answers: LearningStyleAnswers): Promise<LearningStyleResult> {
        return this.request<LearningStyleResult>(`/students/${userId}/learning-style`, {
            method: 'POST',
            body: JSON.stringify({ answers }),
        });
    }

    async getLearningStyle(userId: string): Promise<LearningStyleResult> {
        return this.request<LearningStyleResult>(`/students/${userId}/learning-style`);
    }

    // ==================== DOUBT SOLVER ENDPOINTS ====================
    async askDoubt(question: string, subject?: string | null): Promise<{
        answer: string;
        sources?: Array<{
            text: string;
            subject?: string;
            chapter?: string;
            source?: string;
            relevance_score: number;
        }>;
    }> {
        return this.request('/doubt/ask', {
            method: 'POST',
            body: JSON.stringify({
                question,
                subject: subject || null,
                context_limit: 3,
                include_sources: true,
            }),
        });
    }
}

// Export singleton instance
export const api = new ApiClient(API_BASE);
export default api;
