"use client";

import { useRef, useState, useCallback, useMemo } from 'react';
import ReactFlow, {
  Node,
  Edge,
  addEdge,
  Connection,
  Controls,
  Background,
  applyNodeChanges,
  applyEdgeChanges,
  MarkerType,
  ReactFlowInstance,
  Position,
} from 'reactflow';
import 'reactflow/dist/style.css';
import { 
  Brain, 
  Loader2, 
  Sparkles, 
  RefreshCw, 
  CornerDownLeft, 
  ZoomIn, 
  ZoomOut, 
  Maximize2 
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import dagre from 'dagre';

// ---------------------- Types ----------------------
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
}

// ---------------------- Subject Colors ----------------------
const SUBJECT_COLORS: Record<string, string> = {
  Physics: "#60a5fa",
  Chemistry: "#fb7185",
  Math: "#34d399",
  Computer: "#a78bfa",
  default: "#94a3b8",
};

// ---------------------- Dagre layout util ----------------------
const dagreGraph = new dagre.graphlib.Graph();
dagreGraph.setDefaultEdgeLabel(() => ({}));

const getDagreLayout = (
  nodes: Node[],
  edges: Edge[],
  direction: "LR" | "TB" = "LR"
) => {
  const nodeWidth = 280;
  const nodeHeight = 100;

  dagreGraph.setGraph({
    rankdir: direction,
    nodesep: 60,
    ranksep: 120,
    marginx: 25,
    marginy: 25,
  });

  nodes.forEach((n) =>
    dagreGraph.setNode(n.id, { width: nodeWidth, height: nodeHeight })
  );
  edges.forEach((e) => dagreGraph.setEdge(e.source, e.target));
  dagre.layout(dagreGraph);

  const layoutedNodes = nodes.map((n) => {
    const nodeWithPosition = dagreGraph.node(n.id);
    return {
      ...n,
      position: {
        x: nodeWithPosition.x - nodeWidth / 2,
        y: nodeWithPosition.y - nodeHeight / 2,
      },
    };
  });

  edges = edges.map((e) => ({ ...e, type: "straight" }));
  return { nodes: layoutedNodes, edges };
};

// ---------------------- Custom Node Component ----------------------
function CustomNodeContent({ data }: { data: MindMapNode }) {
  const color = SUBJECT_COLORS[data.subject || "default"];
  const badge =
    data.difficulty_level === "beginner"
      ? "bg-emerald-100 text-emerald-700"
      : data.difficulty_level === "intermediate"
      ? "bg-amber-100 text-amber-700"
      : "bg-rose-100 text-rose-700";

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      className="w-[260px] bg-white border border-gray-200 rounded-xl shadow-sm"
      style={{ borderLeft: `6px solid ${color}` }}
    >
      <div className="p-3">
        <h4 className="text-[15px] font-semibold text-slate-900 truncate">
          {data.label}
        </h4>
        <p className="text-[12px] text-slate-600 mt-1 line-clamp-2">
          {data.summary}
        </p>

        <div className="flex items-center gap-2 mt-3">
          <span
            className={`text-[11px] px-2 py-1 rounded-full font-medium ${badge}`}
          >
            {data.difficulty_level}
          </span>
          {data.subject && (
            <span className="text-[11px] text-slate-500 bg-slate-100 px-2 py-1 rounded">
              {data.subject}
            </span>
          )}
        </div>

        <details className="mt-3 text-[13px]">
          <summary className="cursor-pointer text-slate-700 font-medium">
            Details
          </summary>
          <div className="mt-2 text-[13px] text-slate-700 space-y-2">
            <p>{data.description}</p>
            {data.examples && (
              <ul className="list-disc list-inside text-[12px] text-slate-600">
                {data.examples.map((ex, i) => (
                  <li key={i}>{ex}</li>
                ))}
              </ul>
            )}
          </div>
        </details>
      </div>
    </motion.div>
  );
}

const nodeTypes = {
  customNode: ({ data }: { data: MindMapNode }) => (
    <CustomNodeContent data={data} />
  ),
};

// ---------------------- Main Component ----------------------
export default function MindMapGenerator() {
  const [topic, setTopic] = useState("");
  const [subject, setSubject] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [mindmapData, setMindmapData] = useState<MindMapResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const [nodes, setNodes] = useState<Node[]>([]);
  const [edges, setEdges] = useState<Edge[]>([]);
  const reactFlowInstanceRef = useRef<ReactFlowInstance | null>(null);
  const [direction, setDirection] = useState<"LR" | "TB">("LR");

  const suggestions = useMemo(
    () => [
      "Polymers",
      "Mechanics",
      "Organic Chemistry",
      "Calculus",
      "Electricity",
      "Thermodynamics",
      "Coordinate Geometry",
      "Optics",
    ],
    []
  );

  const clearGraph = useCallback(() => {
    setNodes([]);
    setEdges([]);
    setMindmapData(null);
    setError(null);
  }, []);

  const convertToFlow = useCallback(
    (data: MindMapResponse) => {
      const flowNodes: Node[] = data.nodes.map((n) => ({
        id: n.id,
        type: "customNode",
        data: n,
        position: { x: Math.random() * 400, y: Math.random() * 200 },
      }));

      const flowEdges: Edge[] = data.edges.map((e) => {
        const color =
          e.relationship_type === "depends_on"
            ? "#f59e0b"
            : e.relationship_type === "prerequisite"
            ? "#10b981"
            : e.relationship_type === "application_of"
            ? "#8b5cf6"
            : "#3b82f6";

        return {
          id: e.id,
          source: e.source,
          target: e.target,
          label: e.label,
          type: "straight",
          markerEnd: { type: MarkerType.ArrowClosed, color },
          style: { stroke: color, strokeWidth: 2.5 },
          labelStyle: { fontSize: 12, fill: "#334155" },
        } as Edge;
      });

      const laid = getDagreLayout(flowNodes, flowEdges, direction);
      laid.edges = laid.edges.map((e) => ({
        ...e,
        type: "straight",
      }));
      return laid;
    },
    [direction]
  );

  const generateMindMap = useCallback(async () => {
    if (!topic.trim()) {
      setError("Please enter a topic");
      return;
    }
    setIsLoading(true);
    setError(null);

    try {
      const res = await fetch("/api/v1/mindmap/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          topic: topic.trim(),
          subject: subject || null,
          max_nodes: 8,
          include_examples: true,
        }),
      });

      if (!res.ok) throw new Error(`HTTP ${res.status}`);

      const data: MindMapResponse = await res.json();
      if (!data.nodes?.length) throw new Error("No nodes returned");

      const laid = convertToFlow(data);
      setMindmapData(data);
      setNodes(laid.nodes);
      setEdges(laid.edges);

      setTimeout(
        () =>
          reactFlowInstanceRef.current?.fitView({
            padding: 0.15,
            includeHiddenNodes: true,
          }),
        100
      );
    } catch (err: any) {
      setError(err.message);
      clearGraph();
    } finally {
      setIsLoading(false);
    }
  }, [topic, subject, convertToFlow, clearGraph]);

  const toggleDirection = () => {
    const newDir = direction === "LR" ? "TB" : "LR";
    setDirection(newDir);
    const laid = getDagreLayout(nodes, edges, newDir);
    setNodes(laid.nodes);
    setEdges(laid.edges);
  };

  return (
    <div className="h-[calc(100vh-5.5rem)] flex flex-col gap-4">
      <Card>
        <CardContent className="p-5">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-primary/10 rounded-lg">
              <Sparkles className="text-primary" size={22} />
            </div>
            <div>
              <h2 className="text-xl font-semibold">AI Mind Map Generator</h2>
              <p className="text-sm text-muted-foreground">
                Visualize JEE concepts and their relationships
              </p>
            </div>
          </div>

          <div className="mt-4 flex gap-3 flex-wrap items-end">
            <div className="flex-1 min-w-[250px]">
              <label className="text-sm font-medium mb-1 block">Topic</label>
              <Input
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
                placeholder="e.g., Optics, Polymers..."
                onKeyDown={(e) => e.key === "Enter" && generateMindMap()}
              />
            </div>
            <div className="w-48">
              <label className="text-sm font-medium mb-1 block">Subject</label>
              <select
                value={subject}
                onChange={(e) => setSubject(e.target.value)}
                className="w-full border px-3 py-2 rounded-md bg-background"
              >
                <option value="">All</option>
                <option value="Physics">Physics</option>
                <option value="Chemistry">Chemistry</option>
                <option value="Math">Mathematics</option>
                <option value="Computer">Computer Science</option>
              </select>
            </div>
            <Button onClick={generateMindMap} disabled={isLoading}>
              {isLoading ? (
                <Loader2 size={16} className="animate-spin mr-2" />
              ) : (
                <Sparkles size={16} className="mr-2" />
              )}
              Generate
            </Button>
            <Button variant="ghost" onClick={clearGraph}>
              <RefreshCw size={16} />
            </Button>
          </div>

          <div className="mt-3 flex flex-wrap gap-2">
            {suggestions.map((s) => (
              <Button
                key={s}
                variant="secondary"
                size="sm"
                onClick={() => setTopic(s)}
              >
                {s}
              </Button>
            ))}
          </div>

          {error && (
            <div className="mt-3 p-3 bg-rose-50 border border-rose-200 rounded">
              <div className="flex items-center gap-2">
                <CornerDownLeft size={16} className="text-rose-600" />
                <p className="text-sm text-rose-700">{error}</p>
              </div>
            </div>
          )}
        </CardContent>
      </Card>

      <div className="flex-1 relative border rounded-lg overflow-hidden">
        <div className="absolute z-40 top-3 left-3 flex gap-2">
          <Card>
            <CardContent className="p-2 flex gap-2">
              <Button variant="ghost" size="icon" onClick={toggleDirection}>
                <Maximize2 size={16} />
              </Button>
              <Button
                variant="ghost"
                size="icon"
                onClick={() => reactFlowInstanceRef.current?.fitView()}
              >
                <ZoomIn size={16} />
              </Button>
              <Button
                variant="ghost"
                size="icon"
                onClick={() => reactFlowInstanceRef.current?.zoomTo(1.0)}
              >
                <ZoomOut size={16} />
              </Button>
            </CardContent>
          </Card>
        </div>

        <div className="h-full">
          <AnimatePresence>
            {isLoading && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="absolute inset-0 z-50 flex items-center justify-center bg-white/70 backdrop-blur-sm"
              >
                <Loader2 className="animate-spin text-primary" size={40} />
              </motion.div>
            )}
          </AnimatePresence>

          {nodes.length > 0 ? (
            <ReactFlow
              nodes={nodes}
              edges={edges}
              nodeTypes={nodeTypes}
              fitView
              onInit={(rfi) => (reactFlowInstanceRef.current = rfi)}
              attributionPosition={null}
              style={{ width: "100%", height: "100%" }}
            >
              <Controls showInteractive={true} />
              <Background color="#e5e7eb" gap={20} />
            </ReactFlow>
          ) : (
            <div className="h-full flex items-center justify-center">
              <div className="text-center">
                <div className="bg-primary/10 p-4 rounded-full inline-block mb-3">
                  <Brain className="text-primary" size={44} />
                </div>
                <h3 className="text-lg font-semibold">
                  Generate your first mind map
                </h3>
                <p className="text-sm text-muted-foreground mt-2">
                  Enter a topic above and click Generate.
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}