"use client";

import dynamic from 'next/dynamic';
import { AppLayout } from '@/components/app-layout';
import { Loader2 } from 'lucide-react';

const MindMapGenerator = dynamic(
  () => import('../components/MindMap/MindMapGenerator'),
  {
    loading: () => (
      <div className="flex items-center justify-center h-[calc(100vh-12rem)]">
        <div className="text-center">
          <Loader2 className="h-8 w-8 animate-spin text-primary mx-auto mb-4" />
          <p className="text-muted-foreground">Loading Mind Map Generator...</p>
        </div>
      </div>
    ),
    ssr: false,
  }
);

export default function MindMapPage() {
  return (
    <AppLayout title="Mind Map Generator" showBackButton>
      <MindMapGenerator />
    </AppLayout>
  );
}
