import { useState, useCallback } from 'react';
import { api } from '@/app/api/client';
import { RLQuizQuestion } from '@/app/api/types';

export function useRLSession() {
    const [sessionId, setSessionId] = useState<string | null>(null);
    const [currentQuestion, setCurrentQuestion] = useState<RLQuizQuestion | null>(null);
    const [loading, setLoading] = useState(false);
    const [mastery, setMastery] = useState(0.5);
    const [isFinished, setIsFinished] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const startSession = useCallback(async (studentId: string) => {
        setLoading(true);
        setError(null);
        try {
            const data = await api.startRLSession(studentId);
            setSessionId(data.session_id);
            setCurrentQuestion(data.question);
            setMastery(data.mastery);
            setIsFinished(false);
        } catch (err: any) {
            console.error("Failed to start session", err);
            setError(err.message || "Failed to start session");
        } finally {
            setLoading(false);
        }
    }, []);

    const submitAnswer = useCallback(async (answer: string, isCorrect: boolean) => {
        if (!sessionId) return;
        setLoading(true);
        setError(null);
        try {
            const data = await api.submitRLAnswer(sessionId, answer, isCorrect);
            setMastery(data.mastery);
            
            if (data.done) {
                setIsFinished(true);
                setCurrentQuestion(null);
            } else {
                setCurrentQuestion(data.next_question);
            }
            return data;
        } catch (err: any) {
            console.error("Failed to submit answer", err);
            setError(err.message || "Failed to submit answer");
        } finally {
            setLoading(false);
        }
    }, [sessionId]);

    return {
        sessionId,
        currentQuestion,
        loading,
        mastery,
        isFinished,
        error,
        startSession,
        submitAnswer
    };
}
