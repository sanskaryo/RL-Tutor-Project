import { useState, useEffect } from 'react';
import axios from 'axios';

const useRLSession = () => {
    const [currentQuestion, setCurrentQuestion] = useState(null);
    const [questionNumber, setQuestionNumber] = useState(0);
    const [correctAnswers, setCorrectAnswers] = useState(0);
    const [loading, setLoading] = useState(true);
    const [sessionHistory, setSessionHistory] = useState([]);

    const fetchNextQuestion = async () => {
        setLoading(true);
        try {
            const response = await axios.get('/api/quiz/next-question');
            setCurrentQuestion(response.data);
            setLoading(false);
        } catch (error) {
            console.error('Error fetching the next question:', error);
            setLoading(false);
        }
    };

    const submitAnswer = (userAnswer) => {
        const isCorrect = userAnswer === currentQuestion.answer;
        if (isCorrect) {
            setCorrectAnswers(correctAnswers + 1);
        }
        setSessionHistory([...sessionHistory, { question: currentQuestion, userAnswer, isCorrect }]);
        setQuestionNumber(questionNumber + 1);
        fetchNextQuestion();
    };

    useEffect(() => {
        fetchNextQuestion();
    }, []);

    return {
        currentQuestion,
        questionNumber,
        correctAnswers,
        loading,
        submitAnswer,
        sessionHistory,
    };
};

export default useRLSession;