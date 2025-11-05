"use client";

import { useState, useCallback, useMemo } from 'react';
import ReactFlow, {
  Node,
  Edge,
  addEdge,
  Connection,
  useNodesState,
  useEdgesState,
  Controls,
  Background,
  MiniMap,
  Panel,
} from 'reactflow';
import 'reactflow/dist/style.css';
import { Brain, Loader2, Search, RefreshCw, Info, BookOpen, Download, Sparkles } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { cn } from '@/lib/utils';
import dagre from 'dagre';

// Types
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

interface MindMapEdge {
  id: string;
  source: string;
  target: string;
  label: string;
  relationship_type: string;
}

interface MindMapResponse {
  nodes: MindMapNode[];
  edges: MindMapEdge[];
  topic: string;
  subject?: string;
  generated_at: string;
  mermaid_mindmap?: string;
}

// Custom node component
function CustomNode({ data }: { data: MindMapNode }) {
  const [showDetails, setShowDetails] = useState(false);

  return (
    <motion.div
      initial={{ scale: 0.8, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      transition={{ duration: 0.3 }}
      className="bg-card border-2 border-primary/20 rounded-lg p-3 shadow-lg min-w-[200px] max-w-[300px] hover:shadow-xl transition-shadow"
    >
      <div className="flex items-center justify-between mb-2">
        <h3 className="font-semibold text-sm text-foreground truncate">{data.label}</h3>
        <Button
          variant="ghost"
          size="icon"
          className="h-6 w-6"
          onClick={() => setShowDetails(!showDetails)}
        >
          <Info size={14} />
        </Button>
      </div>

      <p className="text-xs text-muted-foreground mb-2 line-clamp-2">{data.summary}</p>

      <div className="flex items-center gap-2 text-xs">
        <span className={cn(
          "px-2 py-1 rounded-full font-medium",
          data.difficulty_level === 'beginner' && 'bg-accent/20 text-accent',
          data.difficulty_level === 'intermediate' && 'bg-yellow-500/20 text-yellow-700 dark:text-yellow-400',
          data.difficulty_level === 'advanced' && 'bg-destructive/20 text-destructive'
        )}>
          {data.difficulty_level}
        </span>
        {data.subject && (
          <span className="bg-primary/10 text-primary px-2 py-1 rounded-full">
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
            className="mt-3 p-3 bg-muted/50 rounded border border-border max-h-64 overflow-y-auto"
          >
            <h4 className="font-medium text-sm mb-2">Description</h4>
            <p className="text-xs text-foreground/80 mb-3">{data.description}</p>

            {data.examples && data.examples.length > 0 && (
              <div className="mb-3">
                <h4 className="font-medium text-sm mb-1">Examples</h4>
                <ul className="text-xs text-foreground/80 space-y-1">
                  {data.examples.map((example, idx) => (
                    <li key={idx} className="flex items-start">
                      <span className="text-primary mr-1">•</span>
                      {example}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            <div>
              <h4 className="font-medium text-sm mb-1">Related Concepts</h4>
              <div className="flex flex-wrap gap-1">
                {data.related_concepts.map((concept, idx) => (
                  <span key={idx} className="text-xs bg-primary/10 text-primary px-2 py-1 rounded-full">
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

// Node types
const nodeTypes = {
  custom: CustomNode,
};

export default function MindMapGenerator() {
  const [topic, setTopic] = useState('');
  const [subject, setSubject] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [mindmapData, setMindmapData] = useState<MindMapResponse | null>(null);
  const [error, setError] = useState('');
  const [mermaidMap, setMermaidMap] = useState<string>('');

  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);

  // Layout function using dagre
  const getLayoutedElements = useCallback((nodes: Node[], edges: Edge[]) => {
    const dagreGraph = new dagre.graphlib.Graph();
    dagreGraph.setDefaultEdgeLabel(() => ({}));

    const nodeWidth = 250;
    const nodeHeight = 150;

    dagreGraph.setGraph({ rankdir: 'TB' });

    nodes.forEach((node) => {
      dagreGraph.setNode(node.id, { width: nodeWidth, height: nodeHeight });
    });

    edges.forEach((edge) => {
      dagreGraph.setEdge(edge.source, edge.target);
    });

    dagre.layout(dagreGraph);

    const layoutedNodes = nodes.map((node) => {
      const nodeWithPosition = dagreGraph.node(node.id);
      return {
        ...node,
        position: {
          x: nodeWithPosition.x - nodeWidth / 2,
          y: nodeWithPosition.y - nodeHeight / 2,
        },
      };
    });

    return { nodes: layoutedNodes, edges };
  }, []);

  // Convert API response to React Flow format
  const convertToFlowFormat = useCallback((data: MindMapResponse) => {
    const flowNodes: Node[] = data.nodes.map((node, index) => ({
      id: node.id,
      type: 'custom',
      position: { x: 0, y: 0 }, // Will be set by layout
      data: node,
    }));

    const flowEdges: Edge[] = data.edges.map((edge) => ({
      id: edge.id,
      source: edge.source,
      target: edge.target,
      label: edge.label,
      type: 'smoothstep',
      style: { stroke: '#3b82f6', strokeWidth: 2 },
      labelStyle: { fontSize: '12px', fill: '#374151' },
    }));

    return getLayoutedElements(flowNodes, flowEdges);
  }, [getLayoutedElements]);

  const generateMindmap = async () => {
    if (!topic.trim()) {
      setError('Please enter a topic');
      return;
    }

    setIsLoading(true);
    setError('');
    setMermaidMap('');

    try {
      const response = await fetch('/api/v1/mindmap/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          topic: topic.trim(),
          subject: subject || null,
          max_nodes: 8,
          include_examples: true,
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data: MindMapResponse = await response.json();

      if (!data.nodes || data.nodes.length === 0) {
        throw new Error('No nodes returned. Please try another topic.');
      }

      setMindmapData(data);
      setMermaidMap(data.mermaid_mindmap || '');

      const { nodes: layoutedNodes, edges: layoutedEdges } = convertToFlowFormat(data);
      setNodes(layoutedNodes);
      setEdges(layoutedEdges);

    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to generate mind map');
      console.error('Mind map generation error:', err);
      setMindmapData(null);
      setNodes([]);
      setEdges([]);
      setMermaidMap('');
    } finally {
      setIsLoading(false);
    }
  };

  const onConnect = useCallback(
    (params: Connection) => setEdges((eds) => addEdge(params, eds)),
    [setEdges]
  );

  const topicSuggestions = [
    'Polymers', 'Mechanics', 'Organic Chemistry', 'Calculus',
    'Electricity', 'Thermodynamics', 'Coordinate Geometry', 'Optics'
  ];

  return (
    <div className="h-[calc(100vh-8rem)] flex flex-col">
      {/* Header */}
      <Card className="mb-4">
        <CardContent className="p-6">
          <div className="flex items-center gap-3 mb-6">
            <div className="p-2 bg-primary/10 rounded-lg">
              <Sparkles className="text-primary" size={24} />
            </div>
            <div>
              <h1 className="text-2xl font-semibold text-foreground">AI Mind Map Generator</h1>
              <p className="text-sm text-muted-foreground">Visualize JEE concepts and their relationships</p>
            </div>
          </div>

          {/* Input Form */}
          <div className="flex gap-4 items-end flex-wrap">
            <div className="flex-1 min-w-[250px]">
              <label className="block text-sm font-medium mb-2">
                Topic
              </label>
              <Input
                type="text"
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
                placeholder="e.g., Polymers, Mechanics, Organic Chemistry..."
                onKeyPress={(e) => e.key === 'Enter' && generateMindmap()}
              />
            </div>

            <div className="w-48">
              <label className="block text-sm font-medium mb-2">
                Subject (Optional)
              </label>
              <select
                value={subject}
                onChange={(e) => setSubject(e.target.value)}
                className="w-full px-3 py-2 border border-input rounded-md bg-background focus:outline-none focus:ring-2 focus:ring-ring"
              >
                <option value="">All Subjects</option>
                <option value="Physics">Physics</option>
                <option value="Chemistry">Chemistry</option>
                <option value="Math">Mathematics</option>
              </select>
            </div>

            <Button
              onClick={generateMindmap}
              disabled={isLoading}
              size="lg"
              className="gap-2"
            >
              {isLoading ? (
                <Loader2 size={18} className="animate-spin" />
              ) : (
                <Sparkles size={18} />
              )}
              Generate
            </Button>
          </div>

          {/* Topic Suggestions */}
          <div className="mt-4">
            <p className="text-sm text-muted-foreground mb-2">Popular topics:</p>
          <div className="flex flex-wrap gap-2">
            {topicSuggestions.map((suggestion) => (
              <Button
                key={suggestion}
                variant="secondary"
                size="sm"
                onClick={() => setTopic(suggestion)}
              >
                {suggestion}
              </Button>
            ))}
          </div>
        </div>

        {error && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            className="mt-4 p-3 bg-destructive/10 border border-destructive/20 rounded-md"
          >
            <p className="text-sm text-destructive">{error}</p>
          </motion.div>
        )}
      </CardContent>
    </Card>

      {/* Mind Map Display */}
      <div className="flex-1 relative">
        {mindmapData ? (
          <ReactFlow
            nodes={nodes}
            edges={edges}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            onConnect={onConnect}
            nodeTypes={nodeTypes}
            fitView
            attributionPosition="bottom-left"
          >
            <Controls />
            <Background color="#f3f4f6" gap={16} />
            <MiniMap
              nodeColor="#3b82f6"
              maskColor="rgba(255, 255, 255, 0.8)"
            />

            {/* Info Panel */}
            <Panel position="top-right">
              <Card className="min-w-[250px]">
                <CardContent className="p-4">
                  <h3 className="font-semibold text-sm mb-2">{mindmapData.topic}</h3>
                  <div className="space-y-1 text-xs text-muted-foreground">
                    <p>{mindmapData.nodes.length} concepts • {mindmapData.edges.length} connections</p>
                    <p>Generated: {new Date(mindmapData.generated_at).toLocaleTimeString()}</p>
                    {mindmapData.subject && <p>Subject: {mindmapData.subject}</p>}
                  </div>
                </CardContent>
              </Card>
            </Panel>
          </ReactFlow>
        ) : (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="h-full flex items-center justify-center"
          >
            <div className="text-center">
              <div className="p-4 bg-primary/10 rounded-full inline-block mb-4">
                <Brain size={48} className="text-primary" />
              </div>
              <h2 className="text-xl font-semibold mb-2">
                Generate Your First Mind Map
              </h2>
              <p className="text-muted-foreground max-w-md">
                Enter a JEE topic above to create an interactive visual mind map.
                Explore concepts, their relationships, and examples in an engaging way.
              </p>
            </div>
          </motion.div>
        )}
        {mermaidMap && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="absolute bottom-4 left-4 max-w-lg"
          >
            <Card>
              <CardContent className="p-3">
                <div className="flex items-center gap-2 mb-2">
                  <BookOpen size={16} className="text-primary" />
                  <span className="text-xs font-semibold">Mermaid Export</span>
                  <Button
                    variant="ghost"
                    size="sm"
                    className="ml-auto h-6 px-2"
                    onClick={() => navigator.clipboard.writeText(mermaidMap)}
                  >
                    <Download size={12} />
                  </Button>
                </div>
                <pre className="text-[11px] whitespace-pre-wrap max-h-40 overflow-y-auto bg-muted p-2 rounded">
                  {mermaidMap}
                </pre>
              </CardContent>
            </Card>
          </motion.div>
        )}
      </div>
    </div>
  );
}