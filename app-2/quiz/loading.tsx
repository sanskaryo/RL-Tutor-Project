import { Loader2 } from 'lucide-react';

export default function QuizLoading() {
    return (
        <div className="min-h-screen bg-gray-100 flex items-center justify-center">
            <div className="text-center">
                <Loader2 className="w-12 h-12 text-blue-500 animate-spin mx-auto mb-4" />
                <p className="text-gray-800 text-lg font-semibold">Loading Quiz...</p>
                <p className="text-gray-600 text-sm mt-2">Preparing your personalized questions</p>
            </div>
        </div>
    );
}