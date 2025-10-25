'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { useAuth } from '@/app/contexts/AuthContext';
import { api, Content, SessionResponse } from '@/app/api/client';
import Sidebar from '@/app/components/Sidebar';
import { Brain, ArrowRight, CheckCircle, XCircle, Award, Clock } from 'lucide-react';

export default function LearnPage() {
    const router = useRouter();
    const { user, isAuthenticated } = useAuth();

    const [currentContent, setCurrentContent] = useState<Content | null>(null);
    const [selectedAnswer, setSelectedAnswer] = useState('');
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [feedback, setFeedback] = useState<SessionResponse | null>(null);
    const [startTime, setStartTime] = useState<number>(Date.now());
    const [selectedTopic, setSelectedTopic] = useState<string>('');
    const [isLoading, setIsLoading] = useState(false);
    const [sessionStats, setSessionStats] = useState({
        totalQuestions: 0,
        correctAnswers: 0,
        totalReward: 0,
    });

    useEffect(() => {
        if (!isAuthenticated) {
            router.push('/login');
        }
    }, [isAuthenticated]);

    const startSession = async (topic?: string) => {
        if (!user) return;

        try {
            setIsLoading(true);
            setFeedback(null);
            const content = await api.startSession(user, topic);
            setCurrentContent(content);
            setStartTime(Date.now());
            setSelectedAnswer('');
            setSelectedTopic(topic || '');
        } catch (err: any) {
            alert(err.message || 'Failed to start session');
        } finally {
            setIsLoading(false);
        }
    };

    const handleSubmitAnswer = async () => {
        if (!user || !currentContent || !selectedAnswer) return;

        try {
            setIsSubmitting(true);
            const timeSpent = (Date.now() - startTime) / 1000; // Convert to seconds

            const result = await api.submitAnswer(user, {
                session_id: currentContent.id,
                student_answer: selectedAnswer,
                time_spent: timeSpent,
            });

            setFeedback(result);
            setSessionStats(prev => ({
                totalQuestions: prev.totalQuestions + 1,
                correctAnswers: prev.correctAnswers + (result.is_correct ? 1 : 0),
                totalReward: prev.totalReward + result.reward,
            }));
        } catch (err: any) {
            alert(err.message || 'Failed to submit answer');
        } finally {
            setIsSubmitting(false);
        }
    };

    const handleNextQuestion = () => {
        if (feedback?.next_content) {
            setCurrentContent(feedback.next_content);
            setFeedback(null);
            setSelectedAnswer('');
            setStartTime(Date.now());
        } else {
            startSession(selectedTopic || undefined);
        }
    };

    // JEE Subject Topics
    const subjects = [
        {
            name: 'Physics',
            topics: ['mechanics', 'electromagnetism', 'optics', 'modern_physics'],
            description: 'Practice JEE Physics problems',
            icon: '⚛️'
        },
        {
            name: 'Chemistry',
            topics: ['physical_chemistry', 'organic_chemistry', 'inorganic_chemistry'],
            description: 'Practice JEE Chemistry problems',
            icon: '🧪'
        },
        {
            name: 'Mathematics',
            topics: ['algebra', 'calculus', 'coordinate_geometry', 'trigonometry', 'vectors', 'probability'],
            description: 'Practice JEE Mathematics problems',
            icon: '📐'
        }
    ];

    if (!user) {
        return (
            <Sidebar>
                <div className="min-h-screen bg-black flex items-center justify-center text-white">Loading...</div>
            </Sidebar>
        );
    }

    return (
        <Sidebar>
            <div className="min-h-screen bg-black text-white">
                {/* Header */}
                <div className="bg-gradient-to-b from-zinc-900 to-black border-b border-zinc-800">
                    <div className="max-w-7xl mx-auto px-6 py-8">
                        <h1 className="text-3xl font-bold mb-2 flex items-center gap-3">
                            <Brain className="w-8 h-8 text-purple-400" />
                            JEE Practice - Interactive Learning
                        </h1>
                        <p className="text-gray-400">AI-powered adaptive JEE questions tailored to your learning style</p>
                    </div>
                </div>

                <div className="max-w-5xl mx-auto px-6 py-8">
                    {/* Session Stats */}
                    {sessionStats.totalQuestions > 0 && (
                        <div className="bg-zinc-950 border border-zinc-800 rounded-xl p-4 mb-6 flex justify-between items-center">
                            <div className="flex gap-6">
                                <div>
                                    <span className="text-gray-400 text-sm">Questions:</span>
                                    <span className="text-white font-semibold ml-2">{sessionStats.totalQuestions}</span>
                                </div>
                                <div>
                                    <span className="text-gray-400 text-sm">Correct:</span>
                                    <span className="text-green-400 font-semibold ml-2">{sessionStats.correctAnswers}</span>
                                </div>
                                <div>
                                    <span className="text-gray-400 text-sm">Accuracy:</span>
                                    <span className="text-purple-400 font-semibold ml-2">
                                        {((sessionStats.correctAnswers / sessionStats.totalQuestions) * 100).toFixed(0)}%
                                    </span>
                                </div>
                            </div>
                            <div className="flex items-center gap-2">
                                <Award className="w-5 h-5 text-amber-400" />
                                <span className="text-amber-400 font-semibold">+{sessionStats.totalReward.toFixed(1)} pts</span>
                            </div>
                        </div>
                    )}

                    {!currentContent ? (
                        /* Topic Selection */
                        <div className="bg-zinc-950 border border-zinc-800 rounded-xl p-8">
                            <h2 className="text-3xl font-bold mb-4">Choose Your Subject</h2>
                            <p className="text-gray-400 mb-8">Select a subject to start practicing, or let the RL agent pick for you!</p>

                            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                                {subjects.map((subject) => (
                                    <button
                                        key={subject.name}
                                        onClick={() => {
                                            // Pick a random topic from this subject
                                            const randomTopic = subject.topics[Math.floor(Math.random() * subject.topics.length)];
                                            startSession(randomTopic);
                                        }}
                                        disabled={isLoading}
                                        className="p-6 bg-zinc-900 border border-zinc-700 rounded-xl hover:border-purple-500 transition-all duration-200 text-left group disabled:opacity-50"
                                    >
                                        <div className="text-4xl mb-3">{subject.icon}</div>
                                        <h3 className="text-xl font-semibold mb-2 group-hover:text-purple-400">
                                            {subject.name}
                                        </h3>
                                        <p className="text-gray-400 text-sm">{subject.description}</p>
                                    </button>
                                ))}
                            </div>

                            <button
                                onClick={() => startSession()}
                                disabled={isLoading}
                                className="w-full bg-gradient-to-r from-purple-500 to-blue-500 text-white font-semibold py-4 px-6 rounded-xl hover:from-purple-600 hover:to-blue-600 transition-all duration-200 disabled:opacity-50"
                            >
                                {isLoading ? 'Loading...' : 'Let RL Agent Choose (Recommended)'}
                            </button>
                        </div>
                    ) : (
                        /* Question Display */
                        <div className="bg-zinc-950 border border-zinc-800 rounded-xl p-8">
                            {/* Question Header */}
                            <div className="flex justify-between items-start mb-6">
                                <div>
                                    <span className="px-3 py-1 bg-purple-500/20 text-purple-400 rounded-full text-sm font-semibold capitalize">
                                        {currentContent.topic.replace(/_/g, ' ')}
                                    </span>
                                    <span className="ml-3 text-gray-400 text-sm">
                                        Difficulty: {currentContent.difficulty}/10
                                    </span>
                                </div>
                                <div className="flex items-center gap-2 text-gray-400">
                                    <Clock className="w-4 h-4" />
                                    <span className="text-sm">{Math.floor((Date.now() - startTime) / 1000)}s</span>
                                </div>
                            </div>

                            <h2 className="text-2xl font-bold mb-2">{currentContent.title}</h2>
                            <p className="text-xl text-gray-300 mb-8">{currentContent.question_text}</p>

                            {!feedback ? (
                                /* Answer Options */
                                <div className="space-y-3 mb-8">
                                    {currentContent.options && currentContent.options.map((option, idx) => (
                                        <button
                                            key={idx}
                                            onClick={() => setSelectedAnswer(option)}
                                            className={`w-full p-4 rounded-xl border-2 transition-all duration-200 text-left ${selectedAnswer === option
                                                ? 'border-purple-500 bg-purple-500/20'
                                                : 'border-zinc-700 bg-zinc-900 hover:border-zinc-600'
                                                }`}
                                        >
                                            <span className="font-semibold text-lg">{option}</span>
                                        </button>
                                    ))}
                                </div>
                            ) : (
                                /* Feedback Display */
                                <div className={`p-6 rounded-xl mb-8 ${feedback.is_correct
                                    ? 'bg-green-500/10 border-2 border-green-500/50'
                                    : 'bg-red-500/10 border-2 border-red-500/50'
                                    }`}>
                                    <div className="flex items-center gap-3 mb-4">
                                        {feedback.is_correct ? (
                                            <CheckCircle className="w-8 h-8 text-green-400" />
                                        ) : (
                                            <XCircle className="w-8 h-8 text-red-400" />
                                        )}
                                        <h3 className="text-2xl font-bold">
                                            {feedback.is_correct ? 'Correct!' : 'Incorrect'}
                                        </h3>
                                    </div>
                                    <p className="text-lg mb-4">{feedback.explanation}</p>
                                    <div className="flex items-center gap-2">
                                        <Award className="w-5 h-5 text-amber-400" />
                                        <span className="text-amber-400 font-semibold">Reward: +{feedback.reward.toFixed(1)} points</span>
                                    </div>
                                </div>
                            )}

                            {/* Action Buttons */}
                            {!feedback ? (
                                <button
                                    onClick={handleSubmitAnswer}
                                    disabled={!selectedAnswer || isSubmitting}
                                    className="w-full bg-gradient-to-r from-purple-500 to-blue-500 text-white font-semibold py-4 px-6 rounded-xl hover:from-purple-600 hover:to-blue-600 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                                >
                                    {isSubmitting ? 'Submitting...' : 'Submit Answer'}
                                    <ArrowRight className="w-5 h-5" />
                                </button>
                            ) : (
                                <button
                                    onClick={handleNextQuestion}
                                    className="w-full bg-gradient-to-r from-purple-500 to-blue-500 text-white font-semibold py-4 px-6 rounded-xl hover:from-purple-600 hover:to-blue-600 transition-all duration-200 flex items-center justify-center gap-2"
                                >
                                    Next Question
                                    <ArrowRight className="w-5 h-5" />
                                </button>
                            )}
                        </div>
                    )}
                </div>
            </div>
        </Sidebar>
    );
}
