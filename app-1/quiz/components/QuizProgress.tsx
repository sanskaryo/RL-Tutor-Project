import React from 'react';

const QuizProgress = ({ currentQuestion, totalQuestions }) => {
    return (
        <div className="quiz-progress">
            <h3>Quiz Progress</h3>
            <p>
                Question {currentQuestion} of {totalQuestions}
            </p>
        </div>
    );
};

export default QuizProgress;