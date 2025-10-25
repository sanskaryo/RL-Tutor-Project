'use client';

import { useEffect } from 'react';
import Link from 'next/link';
import { AlertTriangle, RefreshCcw, Home } from 'lucide-react';

export default function DashboardError({
    error,
    reset,
}: {
    error: Error & { digest?: string };
    reset: () => void;
}) {
    useEffect(() => {
        console.error('Dashboard error:', error);
    }, [error]);

    return (
        <div className="min-h-screen bg-black flex items-center justify-center px-6">
            <div className="max-w-md w-full text-center">
                <div className="bg-zinc-950 border border-zinc-800 rounded-2xl p-8">
                    <div className="w-16 h-16 bg-red-500/10 rounded-full flex items-center justify-center mx-auto mb-6">
                        <AlertTriangle className="w-8 h-8 text-red-400" />
                    </div>

                    <h1 className="text-3xl font-bold text-white mb-3">
                        Failed to Load Dashboard
                    </h1>

                    <p className="text-gray-400 mb-6">
                        {error.message || 'Could not fetch your dashboard data. Please try again.'}
                    </p>

                    <div className="flex flex-col sm:flex-row gap-3 justify-center">
                        <button
                            onClick={reset}
                            className="px-6 py-3 bg-gradient-to-r from-purple-500 to-blue-500 text-white font-semibold rounded-lg hover:from-purple-600 hover:to-blue-600 transition-all flex items-center justify-center gap-2"
                        >
                            <RefreshCcw className="w-4 h-4" />
                            Retry
                        </button>

                        <Link
                            href="/"
                            className="px-6 py-3 bg-zinc-800 text-white font-semibold rounded-lg hover:bg-zinc-700 transition-all flex items-center justify-center gap-2"
                        >
                            <Home className="w-4 h-4" />
                            Home
                        </Link>
                    </div>
                </div>
            </div>
        </div>
    );
}
