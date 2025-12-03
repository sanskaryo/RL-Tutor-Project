'use client';

import { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useAuth } from '@/app/contexts/AuthContext';
import {
    LayoutDashboard,
    BookOpen,
    Brain,
    TrendingUp,
    Award,
    Calendar,
    Target,
    Sparkles,
    CreditCard,
    BarChart3,
    Settings,
    LogOut,
    Menu,
    X,
    User,
    ChevronLeft,
    Layers
} from 'lucide-react';

interface SidebarProps {
    children: React.ReactNode;
}

export default function Sidebar({ children }: SidebarProps) {
    const [isOpen, setIsOpen] = useState(true);
    const [isMobileOpen, setIsMobileOpen] = useState(false);
    const pathname = usePathname();
    const { user, logout } = useAuth();

    const navigation = [
        { name: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
        { name: 'Learn', href: '/learn', icon: BookOpen },
        { name: 'Flashcards', href: '/flashcards', icon: CreditCard },
        { name: 'Analytics', href: '/analytics', icon: BarChart3 },
        { name: 'Skill Tree', href: '/skill-tree', icon: Layers },
        { name: 'Skill Gaps', href: '/skill-gaps', icon: Target },
        { name: 'Learning Pace', href: '/learning-pace', icon: TrendingUp },
        { name: 'Achievements', href: '/achievements', icon: Award },
        { name: 'Study Plan', href: '/study-plan', icon: Calendar },
        { name: 'RL Viz', href: '/rl-viz', icon: Brain },
        { name: 'AI Quiz', href: '/quiz', icon: Brain },
        { name: 'Learning Style', href: '/learning-style-quiz', icon: Sparkles },
        { name: 'Doubt Solver', href: '/doubt-solver', icon: Brain },
        { name: 'Mind Map', href: '/mindmap', icon: Brain },
    ];

    const isActive = (href: string) => pathname === href;

    return (
        <div className="min-h-screen bg-black flex">
            {/* Desktop Sidebar */}
            <aside
                className={`hidden md:flex flex-col bg-zinc-950 border-r border-zinc-800 transition-all duration-300 fixed h-screen ${isOpen ? 'w-64' : 'w-20'
                    }`}
            >
                {/* Header */}
                <div className="p-4 border-b border-zinc-800 flex items-center justify-between">
                    {isOpen && (
                        <div className="flex items-center gap-2">
                            <Brain className="w-6 h-6 text-purple-400" />
                            <span className="font-bold text-white">RL Tutor</span>
                        </div>
                    )}
                    <button
                        onClick={() => setIsOpen(!isOpen)}
                        className="p-2 hover:bg-zinc-800 rounded-lg transition-colors ml-auto"
                    >
                        {isOpen ? (
                            <ChevronLeft className="w-5 h-5 text-gray-400" />
                        ) : (
                            <Menu className="w-5 h-5 text-gray-400" />
                        )}
                    </button>
                </div>

                {/* Navigation */}
                <nav className="flex-1 p-4 space-y-2 overflow-y-auto">
                    {navigation.map((item) => {
                        const Icon = item.icon;
                        const active = isActive(item.href);

                        return (
                            <Link
                                key={item.name}
                                href={item.href}
                                className={`flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all duration-200 ${active
                                        ? 'bg-purple-500/20 text-purple-400'
                                        : 'text-gray-400 hover:bg-zinc-800 hover:text-white'
                                    } ${!isOpen && 'justify-center'}`}
                                title={!isOpen ? item.name : undefined}
                            >
                                <Icon className="w-5 h-5 flex-shrink-0" />
                                {isOpen && <span className="font-medium">{item.name}</span>}
                            </Link>
                        );
                    })}
                </nav>

                {/* User Section */}
                <div className="p-4 border-t border-zinc-800 space-y-2">
                    {isOpen && user && (
                        <div className="px-3 py-2 bg-zinc-900 rounded-lg mb-2">
                            <div className="flex items-center gap-2 text-sm">
                                <User className="w-4 h-4 text-purple-400" />
                                <span className="text-white font-medium truncate">{user}</span>
                            </div>
                        </div>
                    )}

                    <button
                        onClick={logout}
                        className={`flex items-center gap-3 px-3 py-2.5 rounded-lg text-gray-400 hover:bg-red-500/20 hover:text-red-400 transition-all duration-200 w-full ${!isOpen && 'justify-center'
                            }`}
                        title={!isOpen ? 'Logout' : undefined}
                    >
                        <LogOut className="w-5 h-5 flex-shrink-0" />
                        {isOpen && <span className="font-medium">Logout</span>}
                    </button>
                </div>
            </aside>

            {/* Mobile Sidebar */}
            <div className="md:hidden">
                {/* Mobile Header */}
                <div className="fixed top-0 left-0 right-0 z-50 bg-zinc-950 border-b border-zinc-800 px-4 py-3 flex items-center justify-between">
                    <div className="flex items-center gap-2">
                        <Brain className="w-6 h-6 text-purple-400" />
                        <span className="font-bold text-white">RL Tutor</span>
                    </div>
                    <button
                        onClick={() => setIsMobileOpen(!isMobileOpen)}
                        className="p-2 hover:bg-zinc-800 rounded-lg transition-colors"
                    >
                        {isMobileOpen ? (
                            <X className="w-6 h-6 text-gray-400" />
                        ) : (
                            <Menu className="w-6 h-6 text-gray-400" />
                        )}
                    </button>
                </div>

                {/* Mobile Menu Overlay */}
                {isMobileOpen && (
                    <>
                        <div
                            className="fixed inset-0 bg-black/60 z-40"
                            onClick={() => setIsMobileOpen(false)}
                        />
                        <div className="fixed inset-y-0 left-0 z-50 w-64 bg-zinc-950 border-r border-zinc-800 flex flex-col pt-16">
                            <nav className="flex-1 p-4 space-y-2 overflow-y-auto">
                                {navigation.map((item) => {
                                    const Icon = item.icon;
                                    const active = isActive(item.href);

                                    return (
                                        <Link
                                            key={item.name}
                                            href={item.href}
                                            onClick={() => setIsMobileOpen(false)}
                                            className={`flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all duration-200 ${active
                                                    ? 'bg-purple-500/20 text-purple-400'
                                                    : 'text-gray-400 hover:bg-zinc-800 hover:text-white'
                                                }`}
                                        >
                                            <Icon className="w-5 h-5 flex-shrink-0" />
                                            <span className="font-medium">{item.name}</span>
                                        </Link>
                                    );
                                })}
                            </nav>

                            {/* Mobile User Section */}
                            <div className="p-4 border-t border-zinc-800 space-y-2">
                                {user && (
                                    <div className="px-3 py-2 bg-zinc-900 rounded-lg mb-2">
                                        <div className="flex items-center gap-2 text-sm">
                                            <User className="w-4 h-4 text-purple-400" />
                                            <span className="text-white font-medium truncate">{user}</span>
                                        </div>
                                    </div>
                                )}

                                <button
                                    onClick={() => {
                                        logout();
                                        setIsMobileOpen(false);
                                    }}
                                    className="flex items-center gap-3 px-3 py-2.5 rounded-lg text-gray-400 hover:bg-red-500/20 hover:text-red-400 transition-all duration-200 w-full"
                                >
                                    <LogOut className="w-5 h-5 flex-shrink-0" />
                                    <span className="font-medium">Logout</span>
                                </button>
                            </div>
                        </div>
                    </>
                )}
            </div>

            {/* Main Content */}
            <main className={`flex-1 overflow-auto md:pt-0 pt-16 transition-all duration-300 ${isOpen ? 'md:ml-64' : 'md:ml-20'
                }`}>
                {children}
            </main>
        </div>
    );
}
