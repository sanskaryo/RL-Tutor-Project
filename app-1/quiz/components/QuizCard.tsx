import React, { useState } from 'react';

interface QuizCardProps {
    question: string;
    choices: string[];
    correctAnswer: string;
    onAnswer: (answer: string) => void;
}

const QuizCard: React.FC<QuizCardProps> = ({ question, choices, correctAnswer, onAnswer }) => {
    const [userAnswer, setUserAnswer] = useState<string | null>(null);
    const [feedback, setFeedback] = useState<string | null>(null);

    const handleSubmit = () => {
        if (userAnswer) {
            const isCorrect = userAnswer === correctAnswer;
            setFeedback(isCorrect ? "Correct! 🎉" : `Not quite. The correct answer was: ${correctAnswer}`);
            onAnswer(userAnswer);
        }
    };

    return (
        <div className="quiz-card">
            <h2 className="question">{question}</h2>
            <div className="choices">
                {choices.map((choice, index) => (
                    <label key={index}>
                        <input
                            type="radio"
                            name="quiz-choice"
                            value={choice}
                            checked={userAnswer === choice}
                            onChange={() => setUserAnswer(choice)}
                        />
                        {choice}
                    </label>
                ))}
            </div>
            <button onClick={handleSubmit} disabled={!userAnswer}>
                Submit Answer
            </button>
            {feedback && <p className="feedback">{feedback}</p>}
        </div>
    );
};

export default QuizCard;