'use client';

import dynamic from 'next/dynamic';
import { Loader2 } from 'lucide-react';

const MindMapGenerator = dynamic(
  () => import('./MindMapGenerator'),
  {
    loading: () => (
      <div className="flex items-center justify-center h-[calc(100vh-8rem)]">
        <div className="text-center">
          <Loader2 className="h-8 w-8 animate-spin text-primary mx-auto mb-4" />
          <p className="text-muted-foreground">Loading Mind Map Generator...</p>
        </div>
      </div>
    ),
    ssr: false,
  }
);

export default MindMapGenerator;