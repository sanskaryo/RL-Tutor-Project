import React from 'react';
import { QuizCard } from './components/QuizCard';
import { QuizProgress } from './components/QuizProgress';
import { QuizSummary } from './components/QuizSummary';
import { useRLSession } from './hooks/useRLSession';
import Loading from './loading';

const QuizLayout = () => {
    const {
        currentQuestion,
        totalQuestions,
        userAnswers,
        score,
        isLoading,
        handleAnswer,
        isQuizComplete,
    } = useRLSession();

    if (isLoading) {
        return <Loading />;
    }

    return (
        <div className="quiz-layout">
            <QuizProgress currentQuestion={currentQuestion} totalQuestions={totalQuestions} />
            {!isQuizComplete ? (
                <QuizCard question={currentQuestion} onAnswer={handleAnswer} />
            ) : (
                <QuizSummary score={score} totalQuestions={totalQuestions} userAnswers={userAnswers} />
            )}
        </div>
    );
};

export default QuizLayout;