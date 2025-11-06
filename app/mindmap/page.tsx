import { AppLayout } from '@/components/app-layout';
import MindMapWithLoading from '../components/MindMap/MindMapWithLoading';

export default function MindMapPage() {
  return (
    <AppLayout title="Mind Map Generator" showBackButton>
      <div className="p-2">
        <MindMapWithLoading />
      </div>
    </AppLayout>
  );
}