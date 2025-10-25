'use client';

import { useState } from 'react';
import Link from 'next/link';
import { Brain, TrendingUp, Zap, Award, Play, ArrowRight, CheckCircle } from 'lucide-react';

export default function DemoPage() {
    const [currentStep, setCurrentStep] = useState(0);
    const [demoUser] = useState({
        username: 'demo_student',
        knowledge: {
            algebra: 0.3,
            calculus: 0.1,
            geometry: 0.5,
            statistics: 0.2
        }
    });

    const demoSteps = [
        {
            title: "Welcome to the RL Tutor Demo",
            description: "Experience how our AI adapts to your learning style",
            icon: Brain
        },
        {
            title: "Student Profile Created",
            description: "Your knowledge state is initialized across all topics",
            icon: CheckCircle
        },
        {
            title: "RL Agent Analyzing",
            description: "The Q-Learning agent is selecting the best content for you",
            icon: Zap
        },
        {
            title: "Content Recommended",
            description: "Based on your knowledge, we recommend starting with Geometry",
            icon: TrendingUp
        },
        {
            title: "Ready to Learn!",
            description: "Your personalized learning journey begins now",
            icon: Award
        }
    ];

    const handleNext = () => {
        if (currentStep < demoSteps.length - 1) {
            setCurrentStep(currentStep + 1);
        }
    };

    const handlePrevious = () => {
        if (currentStep > 0) {
            setCurrentStep(currentStep - 1);
        }
    };

    const StepIcon = demoSteps[currentStep].icon;

    return (
        <div className="min-h-screen bg-black text-white">
            {/* Header */}
            <header className="border-b border-zinc-800 bg-zinc-950/50 backdrop-blur-xl">
                <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
                    <div className="flex items-center gap-3">
                        <Play className="w-8 h-8 text-purple-400" />
                        <h1 className="text-2xl font-bold">Interactive Demo</h1>
                    </div>
                    <Link href="/" className="px-4 py-2 bg-zinc-800 hover:bg-zinc-700 rounded-lg transition-colors">
                        Exit Demo
                    </Link>
                </div>
            </header>

            <div className="max-w-4xl mx-auto px-6 py-16">
                {/* Progress Bar */}
                <div className="mb-12">
                    <div className="flex justify-between items-center mb-4">
                        <span className="text-sm text-gray-400">Demo Progress</span>
                        <span className="text-sm text-purple-400 font-semibold">
                            Step {currentStep + 1} of {demoSteps.length}
                        </span>
                    </div>
                    <div className="w-full bg-zinc-800 rounded-full h-2 overflow-hidden">
                        <div
                            className="bg-gradient-to-r from-purple-500 to-blue-500 h-full transition-all duration-500"
                            style={{ width: `${((currentStep + 1) / demoSteps.length) * 100}%` }}
                        />
                    </div>
                </div>

                {/* Current Step Content */}
                <div className="bg-zinc-950 border border-zinc-800 rounded-2xl p-12 mb-8 text-center">
                    <div className="w-24 h-24 bg-purple-500/20 rounded-full flex items-center justify-center mx-auto mb-6">
                        <StepIcon className="w-12 h-12 text-purple-400" />
                    </div>

                    <h2 className="text-4xl font-bold mb-4">{demoSteps[currentStep].title}</h2>
                    <p className="text-xl text-gray-400 mb-8">{demoSteps[currentStep].description}</p>

                    {/* Step-specific content */}
                    {currentStep === 1 && (
                        <div className="bg-zinc-900 rounded-xl p-6 mb-6">
                            <h3 className="text-lg font-semibold mb-4">Initial Knowledge State</h3>
                            <div className="space-y-3">
                                {Object.entries(demoUser.knowledge).map(([topic, value]) => (
                                    <div key={topic}>
                                        <div className="flex justify-between text-sm mb-1">
                                            <span className="capitalize">{topic}</span>
                                            <span className="text-purple-400">{(value * 100).toFixed(0)}%</span>
                                        </div>
                                        <div className="w-full bg-zinc-800 rounded-full h-2">
                                            <div
                                                className="bg-gradient-to-r from-purple-500 to-blue-500 h-full rounded-full transition-all"
                                                style={{ width: `${value * 100}%` }}
                                            />
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}

                    {currentStep === 2 && (
                        <div className="bg-zinc-900 rounded-xl p-6 mb-6">
                            <h3 className="text-lg font-semibold mb-4">Q-Learning Process</h3>
                            <div className="space-y-2 text-left">
                                <div className="flex items-center gap-2">
                                    <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse" />
                                    <span className="text-sm">Analyzing knowledge state...</span>
                                </div>
                                <div className="flex items-center gap-2">
                                    <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse" />
                                    <span className="text-sm">Consulting Q-table...</span>
                                </div>
                                <div className="flex items-center gap-2">
                                    <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse" />
                                    <span className="text-sm">Calculating optimal action...</span>
                                </div>
                                <div className="flex items-center gap-2">
                                    <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse" />
                                    <span className="text-sm">Balancing exploration vs exploitation...</span>
                                </div>
                            </div>
                        </div>
                    )}

                    {currentStep === 3 && (
                        <div className="bg-zinc-900 rounded-xl p-6 mb-6">
                            <h3 className="text-lg font-semibold mb-4">Recommended Content</h3>
                            <div className="bg-gradient-to-r from-green-500/20 to-emerald-500/20 border border-green-500/30 rounded-lg p-4">
                                <div className="text-2xl font-bold text-green-400 mb-2">Geometry - Level 2</div>
                                <p className="text-sm text-gray-300 mb-2">
                                    "Calculate the area of a circle with radius 5cm"
                                </p>
                                <p className="text-xs text-gray-400">
                                    Selected because you have moderate knowledge (50%) in this topic
                                </p>
                            </div>
                        </div>
                    )}

                    {currentStep === 4 && (
                        <div className="bg-zinc-900 rounded-xl p-6 mb-6">
                            <h3 className="text-lg font-semibold mb-4">What Happens Next?</h3>
                            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                                <div className="bg-zinc-800 rounded-lg p-4">
                                    <div className="text-purple-400 font-semibold mb-2">1. Answer</div>
                                    <p className="text-gray-400">You'll answer the question within a time limit</p>
                                </div>
                                <div className="bg-zinc-800 rounded-lg p-4">
                                    <div className="text-blue-400 font-semibold mb-2">2. Feedback</div>
                                    <p className="text-gray-400">Get instant feedback and earn rewards</p>
                                </div>
                                <div className="bg-zinc-800 rounded-lg p-4">
                                    <div className="text-green-400 font-semibold mb-2">3. Adapt</div>
                                    <p className="text-gray-400">Agent learns and adapts to your performance</p>
                                </div>
                            </div>
                        </div>
                    )}
                </div>

                {/* Navigation Buttons */}
                <div className="flex gap-4 justify-between">
                    <button
                        onClick={handlePrevious}
                        disabled={currentStep === 0}
                        className="px-6 py-3 bg-zinc-800 hover:bg-zinc-700 disabled:opacity-30 disabled:cursor-not-allowed rounded-lg font-semibold transition-all"
                    >
                        Previous
                    </button>

                    {currentStep === demoSteps.length - 1 ? (
                        <Link
                            href="/register"
                            className="px-6 py-3 bg-gradient-to-r from-purple-500 to-blue-500 hover:from-purple-600 hover:to-blue-600 rounded-lg font-semibold flex items-center gap-2 transition-all"
                        >
                            Create Account & Start Learning
                            <ArrowRight className="w-5 h-5" />
                        </Link>
                    ) : (
                        <button
                            onClick={handleNext}
                            className="px-6 py-3 bg-gradient-to-r from-purple-500 to-blue-500 hover:from-purple-600 hover:to-blue-600 rounded-lg font-semibold flex items-center gap-2 transition-all"
                        >
                            Next Step
                            <ArrowRight className="w-5 h-5" />
                        </button>
                    )}
                </div>

                {/* Demo Stats */}
                <div className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div className="bg-zinc-950 border border-zinc-800 rounded-xl p-4 text-center">
                        <div className="text-3xl font-bold text-purple-400 mb-1">17</div>
                        <div className="text-sm text-gray-400">Practice Questions</div>
                    </div>
                    <div className="bg-zinc-950 border border-zinc-800 rounded-xl p-4 text-center">
                        <div className="text-3xl font-bold text-blue-400 mb-1">4</div>
                        <div className="text-sm text-gray-400">Topics Available</div>
                    </div>
                    <div className="bg-zinc-950 border border-zinc-800 rounded-xl p-4 text-center">
                        <div className="text-3xl font-bold text-green-400 mb-1">AI</div>
                        <div className="text-sm text-gray-400">Powered Learning</div>
                    </div>
                </div>
            </div>
        </div>
    );
}
