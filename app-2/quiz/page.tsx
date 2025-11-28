import React from 'react';
import QuizCard from './components/QuizCard';
import QuizProgress from './components/QuizProgress';
import QuizSummary from './components/QuizSummary';
import useRLSession from './hooks/useRLSession';
import Loading from './loading';

const QuizPage = () => {
    const {
        currentQuestion,
        questionNumber,
        totalQuestions,
        isLoading,
        score,
        correctAnswers,
        handleAnswer,
        isQuizComplete,
    } = useRLSession();

    if (isLoading) {
        return <Loading />;
    }

    return (
        <div className="quiz-container">
            <QuizProgress 
                questionNumber={questionNumber} 
                totalQuestions={totalQuestions} 
            />
            {isQuizComplete ? (
                <QuizSummary 
                    score={score} 
                    correctAnswers={correctAnswers} 
                    totalQuestions={totalQuestions} 
                />
            ) : (
                <QuizCard 
                    question={currentQuestion} 
                    onAnswer={handleAnswer} 
                />
            )}
        </div>
    );
};

export default QuizPage;