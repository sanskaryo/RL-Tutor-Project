'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { usePathname, useRouter } from 'next/navigation';
import { Brain, Home, LayoutDashboard, BookOpen, BarChart3, Target, LogOut, Menu, X, Lightbulb, User, Timer, Layers, GitBranch, Award, Calendar } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';

export default function Navigation() {
    const pathname = usePathname();
    const router = useRouter();
    const { isAuthenticated, user, logout } = useAuth();
    const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

    // Navigation items for authenticated users
    const authenticatedNavItems = [
        { name: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
        { name: 'Learn', href: '/learn', icon: BookOpen },
        { name: 'Skill Tree', href: '/skill-tree', icon: GitBranch },
        { name: 'Achievements', href: '/achievements', icon: Award },
        { name: 'Study Plan', href: '/study-plan', icon: Calendar },
        { name: 'Flashcards', href: '/flashcards', icon: Layers },
        { name: 'Learning Style', href: '/learning-style-quiz', icon: Lightbulb },
        { name: 'Analytics', href: '/analytics', icon: BarChart3 },
        { name: 'Skill Gaps', href: '/skill-gaps', icon: Target },
        { name: 'Learning Pace', href: '/learning-pace', icon: Timer },
        { name: 'AI Chat', href: '/chat', icon: Brain },
    ];

    // Navigation items for non-authenticated users
    const publicNavItems = [
        { name: 'Home', href: '/', icon: Home },
    ];

    const navItems = isAuthenticated ? authenticatedNavItems : publicNavItems;

    const handleLogout = () => {
        logout();
        setIsMobileMenuOpen(false);
        router.push('/');
    };

    const isActive = (href: string) => {
        if (href === '/') return pathname === '/';
        return pathname.startsWith(href);
    };

    // Don't show navigation on login/register pages or authenticated pages (sidebar is used instead)
    if (pathname === '/login' || pathname === '/register' || isAuthenticated) {
        return null;
    }

    return (
        <nav className="border-b border-zinc-800/50 bg-black/50 backdrop-blur-xl sticky top-0 z-50">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex justify-between items-center h-16">
                    {/* Logo */}
                    <Link href="/" className="flex items-center gap-2 group">
                        <div className="relative">
                            <Brain className="w-8 h-8 text-purple-400 transition-transform group-hover:scale-110" />
                            <div className="absolute inset-0 bg-purple-400/20 blur-xl rounded-full" />
                        </div>
                        <span className="text-xl font-bold bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent">
                            RL Tutor
                        </span>
                    </Link>

                    {/* Desktop Navigation - Only show auth buttons on landing page */}
                    <div className="hidden md:flex items-center gap-3">
                        <Link
                            href="/login"
                            className="px-6 py-2 text-gray-300 hover:text-white transition-colors font-medium"
                        >
                            Login
                        </Link>
                        <Link
                            href="/register"
                            className="px-6 py-2.5 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 rounded-lg font-medium transition-all shadow-lg shadow-purple-500/20 hover:shadow-purple-500/40"
                        >
                            Get Started
                        </Link>
                    </div>

                    {/* Mobile Menu Button */}
                    <button
                        onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
                        className="md:hidden p-2 rounded-lg hover:bg-zinc-800 transition-colors"
                    >
                        {isMobileMenuOpen ? (
                            <X className="w-6 h-6" />
                        ) : (
                            <Menu className="w-6 h-6" />
                        )}
                    </button>
                </div>

                {/* Mobile Menu */}
                {isMobileMenuOpen && (
                    <div className="md:hidden py-4 space-y-2 border-t border-zinc-800">
                        <Link
                            href="/login"
                            onClick={() => setIsMobileMenuOpen(false)}
                            className="block w-full px-4 py-3 text-center text-gray-300 hover:text-white hover:bg-zinc-800/50 rounded-lg transition-all"
                        >
                            Login
                        </Link>
                        <Link
                            href="/register"
                            onClick={() => setIsMobileMenuOpen(false)}
                            className="block w-full px-4 py-3 text-center bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 rounded-lg font-medium transition-all"
                        >
                            Get Started
                        </Link>
                    </div>
                )}
            </div>
        </nav>
    );
}
