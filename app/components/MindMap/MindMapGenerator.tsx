"use client";

import React, { useCallback, useMemo, useState, useRef } from "react";
import ReactFlow, {
  Edge,
  Controls,
  Background,
  Node,
  MarkerType,
  ReactFlowInstance,
  applyNodeChanges,
  applyEdgeChanges,
  OnNodesChange,
  OnEdgesChange,
} from "reactflow";
import "reactflow/dist/style.css";
import dagre from "dagre";
import { motion, AnimatePresence } from "framer-motion";
import {
  Brain,
  Loader2,
  Sparkles,
  RefreshCw,
  CornerDownLeft,
  ZoomIn,
  ZoomOut,
  Maximize2,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";

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
  const nodeWidth = 240;
  const nodeHeight = 100;

  dagreGraph.setGraph({
    rankdir: direction,
    nodesep: 40,
    ranksep: 80,
    marginx: 20,
    marginy: 20,
  });

  nodes.forEach((n) =>
    dagreGraph.setNode(n.id, { width: nodeWidth, height: nodeHeight })
  );
  edges.forEach ((e) => dagreGraph.setEdge(e.source, e.target));
  dagre.layout(dagreGraph);

  const layoutedNodes = nodes.map((n) => {
    const nodeWithPosition = dagreGraph.node(n.id);
    return {
      ...n,
      position: {
        x: nodeWithPosition.x - nodeWidth / 2,
        y: nodeWithPosition.y - nodeHeight / 2,
      },
      style: {
        ...n.style,
        zIndex: 10,
      },
    };
  });

  edges = edges.map((e) => ({ ...e, type: "smoothstep" }));
  return { nodes: layoutedNodes, edges };
};

// ---------------------- Custom Node Component ----------------------
function CustomNodeContent({ data, isDarkMode }: { data: MindMapNode; isDarkMode?: boolean }) {
  const [isExpanded, setIsExpanded] = useState(false);
  const color = SUBJECT_COLORS[data.subject || "default"];
  const badge =
    data.difficulty_level === "beginner"
      ? "bg-emerald-100 text-emerald-700"
      : data.difficulty_level === "intermediate"
      ? "bg-amber-100 text-amber-700"
      : "bg-rose-100 text-rose-700";

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.8 }}
      animate={{ 
        opacity: 1, 
        scale: 1,
        width: isExpanded ? "340px" : "220px",
      }}
      transition={{ 
        duration: 0.3,
        type: "spring",
        stiffness: 300,
        damping: 25
      }}
      className={`border-2 rounded-lg shadow-lg hover:shadow-xl transition-all cursor-grab active:cursor-grabbing relative ${
        isDarkMode 
          ? "bg-slate-800 border-slate-600" 
          : "bg-white border-gray-300"
      }`}
      style={{ 
        borderLeft: `5px solid ${color}`,
        zIndex: isExpanded ? 1000 : 10,
      }}
    >
      <div className="p-3">
        <h4 className={`text-[13px] font-bold mb-1.5 leading-tight ${
          isDarkMode ? "text-slate-100" : "text-slate-900"
        }`} style={{ color }}>
          {data.label}
        </h4>
        <p className={`text-[11px] leading-snug line-clamp-2 ${
          isDarkMode ? "text-slate-300" : "text-slate-600"
        }`}>
          {data.summary}
        </p>

        <div className="flex items-center gap-1.5 mt-2 flex-wrap">
          <span
            className={`text-[9px] px-2 py-0.5 rounded-full font-semibold ${badge}`}
          >
            {data.difficulty_level}
          </span>
          {data.subject && (
            <span className={`text-[9px] px-2 py-0.5 rounded-full font-medium ${
              isDarkMode 
                ? "text-slate-300 bg-slate-700" 
                : "text-slate-600 bg-slate-200"
            }`}>
              {data.subject}
            </span>
          )}
        </div>

        <details
          className="mt-2 text-[11px] group"
          onToggle={(e) => setIsExpanded(e.currentTarget.open)}
        >
          <summary className={`cursor-pointer font-semibold transition-colors list-none flex items-center gap-1.5 text-[10px] ${
            isDarkMode 
              ? "text-slate-300 hover:text-slate-100" 
              : "text-slate-700 hover:text-slate-900"
          }`}>
            <motion.span
              animate={{ rotate: isExpanded ? 90 : 0 }}
              transition={{ duration: 0.2 }}
              className="text-[8px]"
            >
              ▶
            </motion.span>
            Details
          </summary>
          <AnimatePresence>
            {isExpanded && (
              <motion.div
                initial={{ opacity: 0, height: 0, marginTop: 0 }}
                animate={{ opacity: 1, height: "auto", marginTop: 8 }}
                exit={{ opacity: 0, height: 0, marginTop: 0 }}
                transition={{ duration: 0.25 }}
                className={`text-[10px] space-y-2 max-h-48 overflow-y-auto pr-1 border-t pt-2 ${
                  isDarkMode 
                    ? "text-slate-300 border-slate-600" 
                    : "text-slate-700 border-gray-200"
                }`}
              >
                <p className={isDarkMode ? "text-slate-300 leading-snug" : "text-slate-600 leading-snug"}>
                  {data.description}
                </p>
                {data.examples && data.examples.length > 0 && (
                  <div className={`p-2 rounded ${
                    isDarkMode ? "bg-slate-700" : "bg-slate-50"
                  }`}>
                    <p className={`font-semibold mb-1 flex items-center gap-1 text-[9px] ${
                      isDarkMode ? "text-slate-200" : "text-slate-800"
                    }`}>
                      <span className="text-xs">💡</span> Examples:
                    </p>
                    <ul className={`list-disc list-inside text-[9px] space-y-0.5 pl-1 ${
                      isDarkMode ? "text-slate-300" : "text-slate-600"
                    }`}>
                      {data.examples.map((ex, i) => (
                        <li key={i} className="leading-snug line-clamp-1">
                          {ex}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </motion.div>
            )}
          </AnimatePresence>
        </details>
      </div>
    </motion.div>
  );
}

// Create node types factory
const createNodeTypes = (isDarkMode: boolean) => ({
  customNode: ({ data }: { data: MindMapNode }) => (
    <CustomNodeContent data={data} isDarkMode={isDarkMode} />
  ),
});

// ---------------------- Main Component ----------------------
export default function MindMapGenerator() {
  const [topic, setTopic] = useState("");
  const [subject, setSubject] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isDarkMode, setIsDarkMode] = useState(false);

  const [nodes, setNodes] = useState<Node[]>([]);
  const [edges, setEdges] = useState<Edge[]>([]);
  const reactFlowInstanceRef = useRef<ReactFlowInstance | null>(null);
  const [direction, setDirection] = useState<"LR" | "TB">("LR");

  const nodeTypes = useMemo(() => createNodeTypes(isDarkMode), [isDarkMode]);

  const onNodesChange: OnNodesChange = useCallback(
    (changes) => {
      setNodes((nds) => applyNodeChanges(changes, nds));
    },
    []
  );

  const onEdgesChange: OnEdgesChange = useCallback(
    (changes) => {
      setEdges((eds) => applyEdgeChanges(changes, eds));
    },
    []
  );

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
        const colorMap = {
          depends_on: "#f59e0b",
          prerequisite: "#10b981",
          application_of: "#8b5cf6",
          default: "#3b82f6",
        };
        const color = colorMap[e.relationship_type as keyof typeof colorMap] || colorMap.default;

        return {
          id: e.id,
          source: e.source,
          target: e.target,
          label: e.label,
          type: "smoothstep",
          markerEnd: { 
            type: MarkerType.ArrowClosed, 
            color,
            width: 20,
            height: 20,
          },
          animated: true,
          style: {
            stroke: color,
            strokeWidth: 2.5,
            strokeDasharray: "8, 4",
          },
          labelStyle: { 
            fontSize: 10, 
            fill: "#1e293b", 
            fontWeight: 600,
            background: "white",
            padding: "2px 6px",
            borderRadius: "3px",
          },
          labelBgPadding: [6, 3] as [number, number],
          labelBgBorderRadius: 3,
          labelBgStyle: { 
            fill: "white", 
            fillOpacity: 0.9,
            stroke: color,
            strokeWidth: 1,
          },
        } as Edge;
      });

      const laid = getDagreLayout(flowNodes, flowEdges, direction);
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
      setNodes(laid.nodes);
      setEdges(laid.edges);

      setTimeout(
        () =>
          reactFlowInstanceRef.current?.fitView({
            padding: 0.1,
            includeHiddenNodes: false,
            duration: 600,
            maxZoom: 1,
          }),
        150
      );
    } catch (err: Error | unknown) {
      const errorMessage =
        err instanceof Error ? err.message : "Failed to generate mind map";
      setError(errorMessage);
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
    setTimeout(() => {
      reactFlowInstanceRef.current?.fitView({
        padding: 0.1,
        duration: 600,
        maxZoom: 1,
      });
    }, 100);
  };

  return (
    <div className="w-full h-[calc(100vh-5.5rem)] flex flex-col gap-4">
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

      <div className={`flex-1 w-full relative border rounded-lg overflow-hidden transition-colors ${
        isDarkMode ? "bg-slate-900" : "bg-white"
      }`} style={{ minHeight: '400px' }}>
        <div className="absolute z-40 top-3 left-3 flex gap-2">
          <Card>
            <CardContent className="p-2 flex gap-2">
              <Button 
                variant="ghost" 
                size="icon" 
                onClick={() => setIsDarkMode(!isDarkMode)}
                title="Toggle Dark Mode"
              >
                {isDarkMode ? "☀️" : "🌙"}
              </Button>
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
              onNodesChange={onNodesChange}
              onEdgesChange={onEdgesChange}
              nodesDraggable={true}
              nodesConnectable={false}
              elementsSelectable={true}
              fitView
              fitViewOptions={{
                padding: 0.1,
                includeHiddenNodes: false,
                minZoom: 0.8,
                maxZoom: 1.2,
              }}
              minZoom={0.5}
              maxZoom={1.5}
              defaultEdgeOptions={{
                animated: true,
                type: "smoothstep",
              }}
              onInit={(rfi) => {
                reactFlowInstanceRef.current = rfi;
                setTimeout(() => rfi.fitView({ padding: 0.1, duration: 600, maxZoom: 1 }), 100);
              }}
              style={{ width: "100%", height: "100%" }}
            >
              <Controls 
                showInteractive={true}
                showZoom={true}
                showFitView={true}
                position="top-left"
              />
              <Background 
                color={isDarkMode ? "#475569" : "#cbd5e1"}
                gap={16} 
                size={1}
                style={{ 
                  backgroundColor: isDarkMode ? "#1e293b" : "#f8fafc",
                  transition: "all 0.3s ease"
                }}
              />
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



// "use client";

// import { useRef, useState } from 'react';
// import ReactFlow, {
//   Node,
//   Edge,
//   addEdge,
//   Connection,
//   Controls,
//   Background,
//   applyNodeChanges,
//   applyEdgeChanges,
//   MarkerType,
//   ReactFlowInstance,
//   Position,
// } from 'reactflow';
// import 'reactflow/dist/style.css';
// import { Brain, Loader2, RefreshCw, Sparkles, Handle } from 'lucide-react';
// import { motion } from 'framer-motion';
// import { Button } from '@/components/ui/button';
// import { Card, CardContent } from '@/components/ui/card';
// import { Input } from '@/components/ui/input';
// import dagre from 'dagre';
// import { CustomNode } from './MindMapNode';

// // Types
// interface MindMapNode {
//   id: string;
//   label: string;
//   summary: string;
//   description: string;
//   related_concepts: string[];
//   examples?: string[];
//   subject?: string;
//   difficulty_level: string;
// }

// interface MindMapEdge {
//   id: string;
//   source: string;
//   target: string;
//   label: string;
//   relationship_type: string;
// }

// interface MindMapResponse {
//   nodes: MindMapNode[];
//   edges: MindMapEdge[];
//   topic: string;
//   subject?: string;
//   generated_at: string;
//   mermaid_mindmap?: string;
// }

// // Node types
// const nodeTypes = {
//   custom: CustomNode,
// };

// // export default function MindMapGenerator() {
// //   const [topic, setTopic] = useState('');
// //   const [subject, setSubject] = useState('');
// //   const [isLoading, setIsLoading] = useState(false);
// //   const [mindmapData, setMindmapData] = useState<MindMapResponse | null>(null);
// //   const [error, setError] = useState('');
// //   const [mermaidMap, setMermaidMap] = useState<string>('');

// //   const [nodes, setNodes, onNodesChange] = useNodesState([]);
// //   const [edges, setEdges, onEdgesChange] = useEdgesState([]);

// //   // Layout function using dagre
// //   const getLayoutedElements = useCallback((nodes: Node[], edges: Edge[]) => {
// //     const dagreGraph = new dagre.graphlib.Graph();
// //     dagreGraph.setDefaultEdgeLabel(() => ({}));

// //     const nodeWidth = 250;
// //     const nodeHeight = 150;

// //     dagreGraph.setGraph({ rankdir: 'LR', nodesep: 60, ranksep: 100 });


// //     nodes.forEach((node) => {
// //       dagreGraph.setNode(node.id, { width: nodeWidth, height: nodeHeight });
// //     });

// //     edges.forEach((edge) => {
// //       dagreGraph.setEdge(edge.source, edge.target);
// //     });

// //     dagre.layout(dagreGraph);

// //     const layoutedNodes = nodes.map((node) => {
// //       const nodeWithPosition = dagreGraph.node(node.id);
// //       return {
// //         ...node,
// //         position: {
// //           x: nodeWithPosition.x - nodeWidth / 2,
// //           y: nodeWithPosition.y - nodeHeight / 2,
// //         },
// //       };
// //     });

// //     return { nodes: layoutedNodes, edges };
// //   }, []);

// //   // Convert API response to React Flow format
// //   const convertToFlowFormat = useCallback((data: MindMapResponse) => {
// //     const flowNodes: Node[] = data.nodes.map((node, index) => ({
// //       id: node.id,
// //       type: 'custom',
// //       position: { x: 0, y: 0 }, // Will be set by layout
// //       data: node,
// //     }));

// //     const flowEdges: Edge[] = data.edges.map((edge) => ({
// //       id: edge.id,
// //       source: edge.source,
// //       target: edge.target,
// //       label: edge.label,
// //       type: 'smoothstep',
// //       style: { stroke: '#3b82f6', strokeWidth: 2 },
// //       labelStyle: { fontSize: '12px', fill: '#374151' },
// //     }));

// //     return getLayoutedElements(flowNodes, flowEdges);
// //   }, [getLayoutedElements]);

// //   const generateMindmap = async () => {
// //     if (!topic.trim()) {
// //       setError('Please enter a topic');
// //       return;
// //     }

// //     setIsLoading(true);
// //     setError('');
// //     setMermaidMap('');

// //     try {
// //       const response = await fetch('/api/v1/mindmap/generate', {
// //         method: 'POST',
// //         headers: {
// //           'Content-Type': 'application/json',
// //         },
// //         body: JSON.stringify({
// //           topic: topic.trim(),
// //           subject: subject || null,
// //           max_nodes: 8,
// //           include_examples: true,
// //         }),
// //       });

// //       if (!response.ok) {
// //         throw new Error(`HTTP error! status: ${response.status}`);
// //       }

// //       const data: MindMapResponse = await response.json();

// //       if (!data.nodes || data.nodes.length === 0) {
// //         throw new Error('No nodes returned. Please try another topic.');
// //       }

// //       setMindmapData(data);
// //       setMermaidMap(data.mermaid_mindmap || '');

// //       const { nodes: layoutedNodes, edges: layoutedEdges } = convertToFlowFormat(data);
// //       setNodes(layoutedNodes);
// //       setEdges(layoutedEdges);

// //     } catch (err) {
// //       setError(err instanceof Error ? err.message : 'Failed to generate mind map');
// //       console.error('Mind map generation error:', err);
// //       setMindmapData(null);
// //       setNodes([]);
// //       setEdges([]);
// //       setMermaidMap('');
// //     } finally {
// //       setIsLoading(false);
// //     }
// //   };

// //   const onConnect = useCallback(
// //     (params: Connection) => setEdges((eds) => addEdge(params, eds)),
// //     [setEdges]
// //   );

// //   const topicSuggestions = [
// //     'Polymers', 'Mechanics', 'Organic Chemistry', 'Calculus',
// //     'Electricity', 'Thermodynamics', 'Coordinate Geometry', 'Optics'
// //   ];

// //   return (
// //     <div className="h-[calc(100vh-8rem)] flex flex-col">
// //       {/* Header */}
// //       <Card className="mb-4">
// //         <CardContent className="p-6">
// //           <div className="flex items-center gap-3 mb-6">
// //             <div className="p-2 bg-primary/10 rounded-lg">
// //               <Sparkles className="text-primary" size={24} />
// //             </div>
// //             <div>
// //               <h1 className="text-2xl font-semibold text-foreground">AI Mind Map Generator</h1>
// //               <p className="text-sm text-muted-foreground">Visualize JEE concepts and their relationships</p>
// //             </div>
// //           </div>

// //           {/* Input Form */}
// //           <div className="flex gap-4 items-end flex-wrap">
// //             <div className="flex-1 min-w-[250px]">
// //               <label className="block text-sm font-medium mb-2">
// //                 Topic
// //               </label>
// //               <Input
// //                 type="text"
// //                 value={topic}
// //                 onChange={(e) => setTopic(e.target.value)}
// //                 placeholder="e.g., Polymers, Mechanics, Organic Chemistry..."
// //                 onKeyPress={(e) => e.key === 'Enter' && generateMindmap()}
// //               />
// //             </div>

// //             <div className="w-48">
// //               <label className="block text-sm font-medium mb-2">
// //                 Subject (Optional)
// //               </label>
// //               <select
// //                 value={subject}
// //                 onChange={(e) => setSubject(e.target.value)}
// //                 className="w-full px-3 py-2 border border-input rounded-md bg-background focus:outline-none focus:ring-2 focus:ring-ring"
// //               >
// //                 <option value="">All Subjects</option>
// //                 <option value="Physics">Physics</option>
// //                 <option value="Chemistry">Chemistry</option>
// //                 <option value="Math">Mathematics</option>
// //               </select>
// //             </div>

// //             <Button
// //               onClick={generateMindmap}
// //               disabled={isLoading}
// //               size="lg"
// //               className="gap-2"
// //             >
// //               {isLoading ? (
// //                 <Loader2 size={18} className="animate-spin" />
// //               ) : (
// //                 <Sparkles size={18} />
// //               )}
// //               Generate
// //             </Button>
// //           </div>

// //           {/* Topic Suggestions */}
// //           <div className="mt-4">
// //             <p className="text-sm text-muted-foreground mb-2">Popular topics:</p>
// //           <div className="flex flex-wrap gap-2">
// //             {topicSuggestions.map((suggestion) => (
// //               <Button
// //                 key={suggestion}
// //                 variant="secondary"
// //                 size="sm"
// //                 onClick={() => setTopic(suggestion)}
// //               >
// //                 {suggestion}
// //               </Button>
// //             ))}
// //           </div>
// //         </div>

// //         {error && (
// //           <motion.div
// //             initial={{ opacity: 0, y: -10 }}
// //             animate={{ opacity: 1, y: 0 }}
// //             className="mt-4 p-3 bg-destructive/10 border border-destructive/20 rounded-md"
// //           >
// //             <p className="text-sm text-destructive">{error}</p>
// //           </motion.div>
// //         )}
// //       </CardContent>
// //     </Card>

// //       {/* Mind Map Display */}
// //       <div className="flex-1 relative">
// //         {mindmapData ? (
// //           <ReactFlow
// //             nodes={nodes}
// //             edges={edges}
// //             onNodesChange={onNodesChange}
// //             onEdgesChange={onEdgesChange}
// //             onConnect={onConnect}
// //             nodeTypes={nodeTypes}
// //             fitView
// //             attributionPosition="bottom-left"
// //           >
// //             <Controls />
// //             <Background color="#f3f4f6" gap={16} />
// //             <MiniMap
// //               nodeColor="#3b82f6"
// //               maskColor="rgba(255, 255, 255, 0.8)"
// //             />

// //             {/* Info Panel */}
// //             <Panel position="top-right">
// //               <Card className="min-w-[250px]">
// //                 <CardContent className="p-4">
// //                   <h3 className="font-semibold text-sm mb-2">{mindmapData.topic}</h3>
// //                   <div className="space-y-1 text-xs text-muted-foreground">
// //                     <p>{mindmapData.nodes.length} concepts • {mindmapData.edges.length} connections</p>
// //                     <p>Generated: {new Date(mindmapData.generated_at).toLocaleTimeString()}</p>
// //                     {mindmapData.subject && <p>Subject: {mindmapData.subject}</p>}
// //                   </div>
// //                 </CardContent>
// //               </Card>
// //             </Panel>
// //           </ReactFlow>
// //         ) : (
// //           <motion.div
// //             initial={{ opacity: 0 }}
// //             animate={{ opacity: 1 }}
// //             className="h-full flex items-center justify-center"
// //           >
// //             <div className="text-center">
// //               <div className="p-4 bg-primary/10 rounded-full inline-block mb-4">
// //                 <Brain size={48} className="text-primary" />
// //               </div>
// //               <h2 className="text-xl font-semibold mb-2">
// //                 Generate Your First Mind Map
// //               </h2>
// //               <p className="text-muted-foreground max-w-md">
// //                 Enter a JEE topic above to create an interactive visual mind map.
// //                 Explore concepts, their relationships, and examples in an engaging way.
// //               </p>
// //             </div>
// //           </motion.div>
// //         )}
// //         {mermaidMap && (
// //           <motion.div
// //             initial={{ opacity: 0, y: 20 }}
// //             animate={{ opacity: 1, y: 0 }}
// //             className="absolute bottom-4 left-4 max-w-lg"
// //           >
// //             <Card>
// //               <CardContent className="p-3">
// //                 <div className="flex items-center gap-2 mb-2">
// //                   <BookOpen size={16} className="text-primary" />
// //                   <span className="text-xs font-semibold">Mermaid Export</span>
// //                   <Button
// //                     variant="ghost"
// //                     size="sm"
// //                     className="ml-auto h-6 px-2"
// //                     onClick={() => navigator.clipboard.writeText(mermaidMap)}
// //                   >
// //                     <Download size={12} />
// //                   </Button>
// //                 </div>
// //                 <pre className="text-[11px] whitespace-pre-wrap max-h-40 overflow-y-auto bg-muted p-2 rounded">
// //                   {mermaidMap}
// //                 </pre>
// //               </CardContent>
// //             </Card>
// //           </motion.div>
// //         )}
// //       </div>
// //     </div>
// //   );
// // }

// "use client";

// import React, { useCallback, useMemo, useState, useRef } from "react";
// import ReactFlow, {
//   addEdge,
//   applyEdgeChanges,
//   applyNodeChanges,
//   Connection,
//   Edge,
//   Controls,
//   Background,
//   Node,
//   MarkerType,
//   ReactFlowInstance,
// } from "reactflow";
// import "reactflow/dist/style.css";
// import dagre from "dagre";
// import { motion, AnimatePresence } from "framer-motion";
// import {
//   Brain,
//   Loader2,
//   Sparkles,
//   RefreshCw,
//   CornerDownLeft,
//   ZoomIn,
//   ZoomOut,
//   Maximize2,
// } from "lucide-react";
// import { Button } from "@/components/ui/button";
// import { Card, CardContent } from "@/components/ui/card";
// import { Input } from "@/components/ui/input";

// // ---------------------- Types ----------------------
// interface MindMapNode {
//   id: string;
//   label: string;
//   summary: string;
//   description: string;
//   related_concepts: string[];
//   examples?: string[];
//   subject?: string;
//   difficulty_level: string;
// }

// interface MindMapEdge {
//   id: string;
//   source: string;
//   target: string;
//   label: string;
//   relationship_type: string;
// }

// interface MindMapResponse {
//   nodes: MindMapNode[];
//   edges: MindMapEdge[];
//   topic: string;
//   subject?: string;
//   generated_at: string;
// }

// // ---------------------- Subject Colors ----------------------
// const SUBJECT_COLORS: Record<string, string> = {
//   Physics: "#60a5fa",
//   Chemistry: "#fb7185",
//   Math: "#34d399",
//   Computer: "#a78bfa",
//   default: "#94a3b8",
// };

// // ---------------------- Dagre layout util ----------------------
// const dagreGraph = new dagre.graphlib.Graph();
// dagreGraph.setDefaultEdgeLabel(() => ({}));

// const getDagreLayout = (
//   nodes: Node[],
//   edges: Edge[],
//   direction: "LR" | "TB" = "LR"
// ) => {
//   const nodeWidth = 280;
//   const nodeHeight = 100;

//   dagreGraph.setGraph({
//     rankdir: direction,
//     nodesep: 60,
//     ranksep: 120,
//     marginx: 25,
//     marginy: 25,
//   });

//   nodes.forEach((n) =>
//     dagreGraph.setNode(n.id, { width: nodeWidth, height: nodeHeight })
//   );
//   edges.forEach((e) => dagreGraph.setEdge(e.source, e.target));
//   dagre.layout(dagreGraph);

//   const layoutedNodes = nodes.map((n) => {
//     const nodeWithPosition = dagreGraph.node(n.id);
//     return {
//       ...n,
//       position: {
//         x: nodeWithPosition.x - nodeWidth / 2,
//         y: nodeWithPosition.y - nodeHeight / 2,
//       },
//     };
//   });

//   edges = edges.map((e) => ({ ...e, type: "straight" }));
//   return { nodes: layoutedNodes, edges };
// };

// // ---------------------- Custom Node Component ----------------------
// function CustomNodeContent({ data }: { data: MindMapNode }) {
//   const color = SUBJECT_COLORS[data.subject || "default"];
//   const badge =
//     data.difficulty_level === "beginner"
//       ? "bg-emerald-100 text-emerald-700"
//       : data.difficulty_level === "intermediate"
//       ? "bg-amber-100 text-amber-700"
//       : "bg-rose-100 text-rose-700";

//   return (
//     <motion.div
//       initial={{ opacity: 0, scale: 0.9 }}
//       animate={{ opacity: 1, scale: 1 }}
//       className="w-[260px] bg-white border border-gray-200 rounded-xl shadow-sm"
//       style={{ borderLeft: `6px solid ${color}` }}
//     >
//       <div className="p-3">
//         <h4 className="text-[15px] font-semibold text-slate-900 truncate">
//           {data.label}
//         </h4>
//         <p className="text-[12px] text-slate-600 mt-1 line-clamp-2">
//           {data.summary}
//         </p>

//         <div className="flex items-center gap-2 mt-3">
//           <span
//             className={`text-[11px] px-2 py-1 rounded-full font-medium ${badge}`}
//           >
//             {data.difficulty_level}
//           </span>
//           {data.subject && (
//             <span className="text-[11px] text-slate-500 bg-slate-100 px-2 py-1 rounded">
//               {data.subject}
//             </span>
//           )}
//         </div>

//         <details className="mt-3 text-[13px]">
//           <summary className="cursor-pointer text-slate-700 font-medium">
//             Details
//           </summary>
//           <div className="mt-2 text-[13px] text-slate-700 space-y-2">
//             <p>{data.description}</p>
//             {data.examples && (
//               <ul className="list-disc list-inside text-[12px] text-slate-600">
//                 {data.examples.map((ex, i) => (
//                   <li key={i}>{ex}</li>
//                 ))}
//               </ul>
//             )}
//           </div>
//         </details>
//       </div>
//     </motion.div>
//   );
// }

// const nodeTypes = {
//   customNode: ({ data }: { data: MindMapNode }) => (
//     <CustomNodeContent data={data} />
//   ),
// };

// // ---------------------- Main Component ----------------------
// export default function MindMapGenerator() {
//   const [topic, setTopic] = useState("");
//   const [subject, setSubject] = useState("");
//   const [isLoading, setIsLoading] = useState(false);
//   const [mindmapData, setMindmapData] = useState<MindMapResponse | null>(null);
//   const [error, setError] = useState<string | null>(null);

//   const [nodes, setNodes] = useState<Node[]>([]);
//   const [edges, setEdges] = useState<Edge[]>([]);
//   const reactFlowInstanceRef = useRef<ReactFlowInstance | null>(null);
//   const [direction, setDirection] = useState<"LR" | "TB">("LR");

//   const suggestions = useMemo(
//     () => [
//       "Polymers",
//       "Mechanics",
//       "Organic Chemistry",
//       "Calculus",
//       "Electricity",
//       "Thermodynamics",
//       "Coordinate Geometry",
//       "Optics",
//     ],
//     []
//   );

//   const clearGraph = useCallback(() => {
//     setNodes([]);
//     setEdges([]);
//     setMindmapData(null);
//     setError(null);
//   }, []);

//   const convertToFlow = useCallback(
//     (data: MindMapResponse) => {
//       const flowNodes: Node[] = data.nodes.map((n) => ({
//         id: n.id,
//         type: "customNode",
//         data: n,
//         position: { x: Math.random() * 400, y: Math.random() * 200 },
//       }));

//       const flowEdges: Edge[] = data.edges.map((e) => {
//         const color =
//           e.relationship_type === "depends_on"
//             ? "#f59e0b"
//             : e.relationship_type === "prerequisite"
//             ? "#10b981"
//             : e.relationship_type === "application_of"
//             ? "#8b5cf6"
//             : "#3b82f6";

//         return {
//           id: e.id,
//           source: e.source,
//           target: e.target,
//           label: e.label,
//           type: "straight",
//           markerEnd: { type: MarkerType.ArrowClosed, color },
//           style: { stroke: color, strokeWidth: 2.5 },
//           labelStyle: { fontSize: 12, fill: "#334155" },
//         } as Edge;
//       });

//       const laid = getDagreLayout(flowNodes, flowEdges, direction);
//       laid.edges = laid.edges.map((e) => ({
//         ...e,
//         type: "straight",
//       }));
//       return laid;
//     },
//     [direction]
//   );

//   const generateMindMap = useCallback(async () => {
//     if (!topic.trim()) {
//       setError("Please enter a topic");
//       return;
//     }
//     setIsLoading(true);
//     setError(null);

//     try {
//       const res = await fetch("/api/v1/mindmap/generate", {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify({
//           topic: topic.trim(),
//           subject: subject || null,
//           max_nodes: 8,
//           include_examples: true,
//         }),
//       });

//       if (!res.ok) throw new Error(`HTTP ${res.status}`);

//       const data: MindMapResponse = await res.json();
//       if (!data.nodes?.length) throw new Error("No nodes returned");

//       const laid = convertToFlow(data);
//       setMindmapData(data);
//       setNodes(laid.nodes);
//       setEdges(laid.edges);

//       setTimeout(
//         () =>
//           reactFlowInstanceRef.current?.fitView({
//             padding: 0.15,
//             includeHiddenNodes: true,
//           }),
//         100
//       );
//     } catch (err: any) {
//       setError(err.message);
//       clearGraph();
//     } finally {
//       setIsLoading(false);
//     }
//   }, [topic, subject, convertToFlow, clearGraph]);

//   const toggleDirection = () => {
//     const newDir = direction === "LR" ? "TB" : "LR";
//     setDirection(newDir);
//     const laid = getDagreLayout(nodes, edges, newDir);
//     setNodes(laid.nodes);
//     setEdges(laid.edges);
//   };

//   return (
//     <div className="h-[calc(100vh-5.5rem)] flex flex-col gap-4">
//       <Card>
//         <CardContent className="p-5">
//           <div className="flex items-center gap-3">
//             <div className="p-2 bg-primary/10 rounded-lg">
//               <Sparkles className="text-primary" size={22} />
//             </div>
//             <div>
//               <h2 className="text-xl font-semibold">AI Mind Map Generator</h2>
//               <p className="text-sm text-muted-foreground">
//                 Visualize JEE concepts and their relationships
//               </p>
//             </div>
//           </div>

//           <div className="mt-4 flex gap-3 flex-wrap items-end">
//             <div className="flex-1 min-w-[250px]">
//               <label className="text-sm font-medium mb-1 block">Topic</label>
//               <Input
//                 value={topic}
//                 onChange={(e) => setTopic(e.target.value)}
//                 placeholder="e.g., Optics, Polymers..."
//                 onKeyDown={(e) => e.key === "Enter" && generateMindMap()}
//               />
//             </div>
//             <div className="w-48">
//               <label className="text-sm font-medium mb-1 block">Subject</label>
//               <select
//                 value={subject}
//                 onChange={(e) => setSubject(e.target.value)}
//                 className="w-full border px-3 py-2 rounded-md bg-background"
//               >
//                 <option value="">All</option>
//                 <option value="Physics">Physics</option>
//                 <option value="Chemistry">Chemistry</option>
//                 <option value="Math">Mathematics</option>
//                 <option value="Computer">Computer Science</option>
//               </select>
//             </div>
//             <Button onClick={generateMindMap} disabled={isLoading}>
//               {isLoading ? (
//                 <Loader2 size={16} className="animate-spin mr-2" />
//               ) : (
//                 <Sparkles size={16} className="mr-2" />
//               )}
//               Generate
//             </Button>
//             <Button variant="ghost" onClick={clearGraph}>
//               <RefreshCw size={16} />
//             </Button>
//           </div>

//           <div className="mt-3 flex flex-wrap gap-2">
//             {suggestions.map((s) => (
//               <Button
//                 key={s}
//                 variant="secondary"
//                 size="sm"
//                 onClick={() => setTopic(s)}
//               >
//                 {s}
//               </Button>
//             ))}
//           </div>

//           {error && (
//             <div className="mt-3 p-3 bg-rose-50 border border-rose-200 rounded">
//               <div className="flex items-center gap-2">
//                 <CornerDownLeft size={16} className="text-rose-600" />
//                 <p className="text-sm text-rose-700">{error}</p>
//               </div>
//             </div>
//           )}
//         </CardContent>
//       </Card>

//       <div className="flex-1 relative border rounded-lg overflow-hidden">
//         <div className="absolute z-40 top-3 left-3 flex gap-2">
//           <Card>
//             <CardContent className="p-2 flex gap-2">
//               <Button variant="ghost" size="icon" onClick={toggleDirection}>
//                 <Maximize2 size={16} />
//               </Button>
//               <Button
//                 variant="ghost"
//                 size="icon"
//                 onClick={() => reactFlowInstanceRef.current?.fitView()}
//               >
//                 <ZoomIn size={16} />
//               </Button>
//               <Button
//                 variant="ghost"
//                 size="icon"
//                 onClick={() => reactFlowInstanceRef.current?.zoomTo(1.0)}
//               >
//                 <ZoomOut size={16} />
//               </Button>
//             </CardContent>
//           </Card>
//         </div>

//         <div className="h-full">
//           <AnimatePresence>
//             {isLoading && (
//               <motion.div
//                 initial={{ opacity: 0 }}
//                 animate={{ opacity: 1 }}
//                 exit={{ opacity: 0 }}
//                 className="absolute inset-0 z-50 flex items-center justify-center bg-white/70 backdrop-blur-sm"
//               >
//                 <Loader2 className="animate-spin text-primary" size={40} />
//               </motion.div>
//             )}
//           </AnimatePresence>

//           {nodes.length > 0 ? (
//             <ReactFlow
//               nodes={nodes}
//               edges={edges}
//               nodeTypes={nodeTypes}
//               fitView
//               onInit={(rfi) => (reactFlowInstanceRef.current = rfi)}
//               attributionPosition={null}
//               style={{ width: "100%", height: "100%" }}
//             >
//               <Controls showInteractive={true} />
//               <Background color="#e5e7eb" gap={20} />
//             </ReactFlow>
//           ) : (
//             <div className="h-full flex items-center justify-center">
//               <div className="text-center">
//                 <div className="bg-primary/10 p-4 rounded-full inline-block mb-3">
//                   <Brain className="text-primary" size={44} />
//                 </div>
//                 <h3 className="text-lg font-semibold">
//                   Generate your first mind map
//                 </h3>
//                 <p className="text-sm text-muted-foreground mt-2">
//                   Enter a topic above and click Generate.
//                 </p>
//               </div>
//             </div>
//           )}
//         </div>
//       </div>
//     </div>
//   );
// }
