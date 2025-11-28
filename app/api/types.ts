export interface ProgressResponse {
    total_attempts: number;
    correct_answers: number;
    accuracy_rate: number;
    topics_mastered: string[];
    current_streak: number;
}

export interface RLStats {
    episodes: number;
    rewards: number[];
    avg_reward: number;
    current_state: Record<string, number>;
}

export interface PerformancePoint {
    date: string;
    score: number;
    attempts: number;
}

export interface QuizQuestion {
    id: number;
    text: string;
    options: string[];
}

export interface LearningStyleQuiz {
    questions: QuizQuestion[];
}

export interface LearningStyleAnswers {
    [questionId: string]: string;
}

export interface LearningStyleResult {
    style: string;
    scores: {
        visual: number;
        auditory: number;
        reading: number;
        kinesthetic: number;
    };
    recommendations: string[];
}

export interface RLQuizQuestion {
    text: string;
    id: string;
    type: string;
    choices: string[];
    skill: string;
}

export interface RLSessionStartResponse {
    session_id: string;
    question: RLQuizQuestion;
    mastery: number;
}

export interface RLSubmitResponse {
    correct: boolean;
    reward: number;
    mastery: number;
    done: boolean;
    next_question: RLQuizQuestion | null;
}