'use client';

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect } from "react";
import { useAuth } from "./contexts/AuthContext";
import { Brain, Sparkles, TrendingUp, Award } from "lucide-react";

export default function Home() {
  const router = useRouter();
  const { isAuthenticated } = useAuth();

  useEffect(() => {
    // Redirect to dashboard if already logged in
    if (isAuthenticated) {
      router.push('/dashboard');
    }
  }, [isAuthenticated, router]);

  return (
    <div className="min-h-screen bg-black text-white flex items-center justify-center relative overflow-hidden">
      {/* Animated background gradient */}
      <div className="absolute inset-0 bg-gradient-to-br from-purple-900/20 via-black to-blue-900/20" />
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(120,119,198,0.1),transparent_50%)]" />

      {/* Content */}
      <div className="relative z-10 max-w-5xl mx-auto px-6 py-20 text-center">
        {/* Logo/Icon */}
        <div className="flex justify-center mb-8">
          <div className="relative">
            <div className="absolute inset-0 bg-purple-500/30 blur-3xl rounded-full" />
            <Brain className="w-24 h-24 text-purple-400 relative animate-pulse" />
          </div>
        </div>

        {/* Main Heading */}
        <h1 className="text-6xl md:text-7xl font-bold mb-6 bg-gradient-to-r from-purple-400 via-pink-400 to-blue-400 bg-clip-text text-transparent">
          RL Tutor
        </h1>

        <p className="text-xl md:text-2xl text-gray-300 mb-4">
          AI-Powered Adaptive Learning for JEE
        </p>

        <p className="text-gray-400 mb-12 max-w-2xl mx-auto">
          Master Physics, Chemistry, and Mathematics with personalized learning paths
          powered by Reinforcement Learning algorithms.
        </p>

        {/* CTA Buttons */}
        <div className="flex flex-col sm:flex-row gap-4 justify-center mb-16">
          <Link
            href="/register"
            className="px-8 py-4 bg-gradient-to-r from-purple-500 to-blue-500 rounded-lg font-semibold text-lg hover:from-purple-600 hover:to-blue-600 transition-all duration-200 shadow-lg hover:shadow-purple-500/50"
          >
            Get Started Free
          </Link>
          <Link
            href="/login"
            className="px-8 py-4 bg-white/10 backdrop-blur-sm border border-white/20 rounded-lg font-semibold text-lg hover:bg-white/20 transition-all duration-200"
          >
            Sign In
          </Link>
        </div>

        {/* Features */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-4xl mx-auto">
          <div className="p-6 bg-white/5 backdrop-blur-sm border border-white/10 rounded-xl hover:border-purple-500/50 transition-all duration-200">
            <Sparkles className="w-8 h-8 text-purple-400 mb-3 mx-auto" />
            <h3 className="font-semibold mb-2">Adaptive Learning</h3>
            <p className="text-sm text-gray-400">Questions adapt to your skill level in real-time</p>
          </div>

          <div className="p-6 bg-white/5 backdrop-blur-sm border border-white/10 rounded-xl hover:border-blue-500/50 transition-all duration-200">
            <TrendingUp className="w-8 h-8 text-blue-400 mb-3 mx-auto" />
            <h3 className="font-semibold mb-2">Track Progress</h3>
            <p className="text-sm text-gray-400">Detailed analytics and performance insights</p>
          </div>

          <div className="p-6 bg-white/5 backdrop-blur-sm border border-white/10 rounded-xl hover:border-amber-500/50 transition-all duration-200">
            <Award className="w-8 h-8 text-amber-400 mb-3 mx-auto" />
            <h3 className="font-semibold mb-2">Earn Rewards</h3>
            <p className="text-sm text-gray-400">Unlock badges and achievements as you learn</p>
          </div>
        </div>
      </div>
    </div>
  );
}
