"use client";

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Button } from '@/components/ui/button';
import { Info } from 'lucide-react';
import { cn } from '@/lib/utils';

interface MindMapNode {
  id: string;
  label: string;
  summary: string;
  description: string;
  related_concepts: string[];
  examples?: string[];
  subject?: string;
  difficulty_level: string;
}

// Custom node component
export function CustomNode({ data }: { data: MindMapNode }) {
  const [showDetails, setShowDetails] = useState(false);

  return (
    <motion.div
      initial={{ scale: 0.8, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      whileHover={{ scale: 1.02 }}
      transition={{ type: "spring", stiffness: 400, damping: 20 }}
      className="bg-card border border-primary/20 rounded-lg p-4 shadow-md hover:shadow-lg transition-all min-w-[280px] max-w-[320px] relative group"
    >
      <div className="flex items-center justify-between space-x-2">
        <h3 className="font-semibold text-sm text-foreground truncate flex-1">{data.label}</h3>
        <Button
          variant="ghost"
          size="icon"
          className="h-7 w-7 hover:bg-accent/10 opacity-0 group-hover:opacity-100 transition-opacity absolute -right-2 -top-2"
          onClick={() => setShowDetails(!showDetails)}
        >
          <Info className="h-4 w-4" />
        </Button>
      </div>

      <p className="text-xs text-muted-foreground mt-2 mb-3 line-clamp-2">{data.summary}</p>

      <div className="flex items-center gap-2 text-xs">
        <span className={cn(
          "px-2.5 py-1 rounded-full font-medium transition-colors",
          data.difficulty_level === 'beginner' && 'bg-accent/20 text-accent hover:bg-accent/30',
          data.difficulty_level === 'intermediate' && 'bg-yellow-500/20 text-yellow-700 dark:text-yellow-400 hover:bg-yellow-500/30',
          data.difficulty_level === 'advanced' && 'bg-destructive/20 text-destructive hover:bg-destructive/30'
        )}>
          {data.difficulty_level}
        </span>
        {data.subject && (
          <span className="bg-primary/10 text-primary px-2.5 py-1 rounded-full hover:bg-primary/20 transition-colors">
            {data.subject}
          </span>
        )}
      </div>

      <AnimatePresence>
        {showDetails && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            className="mt-4 p-3 bg-muted/50 rounded border border-border max-h-64 overflow-y-auto"
          >
            <h4 className="font-medium text-sm mb-2">Description</h4>
            <p className="text-xs text-foreground/80 mb-3">{data.description}</p>

            {data.examples && data.examples.length > 0 && (
              <div className="mb-3">
                <h4 className="font-medium text-sm mb-1">Examples</h4>
                <ul className="text-xs text-foreground/80 space-y-1.5">
                  {data.examples.map((example, idx) => (
                    <li key={idx} className="flex items-start">
                      <span className="text-primary mr-1.5 mt-0.5">•</span>
                      {example}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            <div>
              <h4 className="font-medium text-sm mb-1.5">Related Concepts</h4>
              <div className="flex flex-wrap gap-1.5">
                {data.related_concepts.map((concept, idx) => (
                  <span 
                    key={idx} 
                    className="text-xs bg-primary/10 text-primary px-2 py-1 rounded-full hover:bg-primary/20 transition-colors"
                  >
                    {concept}
                  </span>
                ))}
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
}