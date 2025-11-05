import DoubtSolverChat from '../components/DoubtSolver/DoubtSolverChat';
import { AppLayout } from '@/components/app-layout';

export default function DoubtSolverPage() {
  return (
    <AppLayout title="AI Doubt Solver" showBackButton>
      <div className="container mx-auto max-w-6xl p-6">
        <div className="mb-4">
          <p className="text-muted-foreground">
            Get instant answers to your JEE questions with citations from study materials
          </p>
        </div>
        <DoubtSolverChat />
      </div>
    </AppLayout>
  );
}
