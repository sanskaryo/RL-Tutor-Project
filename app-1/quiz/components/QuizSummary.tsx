import React from 'react';

const QuizSummary = ({ totalQuestions, correctAnswers, feedback }) => {
    return (
        <div className="quiz-summary">
            <h2>Quiz Summary</h2>
            <p>Total Questions: {totalQuestions}</p>
            <p>Correct Answers: {correctAnswers}</p>
            <p>Score: {((correctAnswers / totalQuestions) * 100).toFixed(2)}%</p>
            {feedback && <p>{feedback}</p>}
        </div>
    );
};

export default QuizSummary;