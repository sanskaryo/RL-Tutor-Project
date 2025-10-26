import DoubtSolverChat from '../components/DoubtSolver/DoubtSolverChat';

export default function DoubtSolverPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 p-4">
      <div className="max-w-7xl mx-auto">
        <div className="mb-6">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            AI Doubt Solver
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Get instant answers to your JEE questions with citations from study materials
          </p>
        </div>
        
        <div className="h-[calc(100vh-200px)]">
          <DoubtSolverChat />
        </div>
      </div>
    </div>
  );
}
