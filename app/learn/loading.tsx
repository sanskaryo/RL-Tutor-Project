import { Loader2 } from 'lucide-react';

export default function LearnLoading() {
    return (
        <div className="min-h-screen bg-black flex items-center justify-center">
            <div className="text-center">
                <Loader2 className="w-12 h-12 text-purple-400 animate-spin mx-auto mb-4" />
                <p className="text-white text-lg font-semibold">Preparing Your Lesson...</p>
                <p className="text-gray-400 text-sm mt-2">The RL agent is selecting the best content for you</p>
            </div>
        </div>
    );
}
