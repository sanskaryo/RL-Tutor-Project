# app/api/mindmap.py
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import logging
import json
import re
from datetime import datetime

from app.core.config import settings
from app.services.llm.gemini_client import GeminiClient

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/mindmap", tags=["Mind Map"])

# Request & response models
class MindMapRequest(BaseModel):
    topic: str = Field(..., min_length=2, max_length=200, description="Topic for mind map")
    subject: Optional[str] = Field(None, description="Subject context (e.g., Physics, Math)")
    max_nodes: int = Field(8, ge=3, le=15, description="Maximum nodes")
    include_examples: bool = Field(True, description="Include examples?")

class MindMapNode(BaseModel):
    id: str
    label: str
    summary: str
    description: str
    related_concepts: List[str]
    examples: Optional[List[str]] = None
    subject: Optional[str] = None
    difficulty_level: str

class MindMapEdge(BaseModel):
    id: str
    source: str
    target: str
    label: str
    relationship_type: str

class MindMapResponse(BaseModel):
    nodes: List[MindMapNode]
    edges: List[MindMapEdge]
    topic: str
    subject: Optional[str]
    generated_at: str
    mermaid_mindmap: Optional[str] = None

# Dependency: create Gemini client or fallback mock
def get_gemini_client():
    api_key = getattr(settings, "GEMINI_API_KEY", None)
    if not api_key:
        # return mock client
        class MockClient:
            def generate(self, prompt: str, *args, **kwargs) -> str:
                # very simple fallback JSON
                return json.dumps({
                    "nodes": [
                        {
                            "id": "root_node",
                            "label": "Root Topic",
                            "summary": "Overview of topic.",
                            "description": "This is a fallback node.",
                            "related_concepts": [],
                            "examples": [],
                            "subject": None,
                            "difficulty_level": "beginner"
                        }
                    ],
                    "edges": []
                })
        return MockClient()
    return GeminiClient(api_key=api_key)

def _fallback_mindmap(topic: str, subject: Optional[str]) -> Dict[str, Any]:
    root_id = topic.lower().replace(" ", "_") or "topic_root"
    nodes = [
        {
            "id": root_id,
            "label": topic.title(),
            "summary": f"Overview of {topic}.",
            "description": f"{topic.title()} is a key concept in {subject or 'JEE'} preparation.",
            "related_concepts": [],
            "examples": [],
            "subject": subject,
            "difficulty_level": "intermediate"
        }
    ]
    edges = []
    mermaid = f"mindmap\n  root(({topic.title()}))\n"
    return {"nodes": nodes, "edges": edges, "mermaid_mindmap": mermaid}

def _extract_json_payload(raw: str) -> str:
    if not raw:
        raise ValueError("Empty response from LLM")
    raw = raw.strip()
    if raw.startswith("{") and raw.endswith("}"):
        return raw
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    if match:
        return match.group()
    raise ValueError("Could not extract JSON")

@router.post("/generate", response_model=MindMapResponse)
def generate_mindmap(
    request: MindMapRequest,
    gemini_client: GeminiClient = Depends(get_gemini_client)
):
    """
    Generate a mind map using Gemini AI with fallback if parsing fails.
    """
    try:
        # 1️⃣ Improved prompt — forces JSON output
        prompt = f"""
        You are an expert JEE tutor for Physics, Chemistry, and Math.
        Create a clear mind map for the topic: "{request.topic}".
        Subject: "{request.subject or 'General'}".
        Limit total nodes to {request.max_nodes} and include examples: {request.include_examples}.

        Respond **ONLY** with valid JSON like this:
        {{
          "nodes": [
            {{
              "id": "calculus_basics",
              "label": "Calculus Basics",
              "summary": "Fundamentals of limits and derivatives",
              "description": "Covers continuity, differentiation and limits for JEE preparation.",
              "related_concepts": ["limits", "continuity", "differentiation"],
              "examples": ["lim x→0 sin(x)/x = 1", "d/dx(x^2) = 2x"],
              "subject": "Math",
              "difficulty_level": "intermediate"
            }}
          ],
          "edges": [
            {{
              "id": "edge_1",
              "source": "calculus_basics",
              "target": "derivatives_intro",
              "label": "prerequisite",
              "relationship_type": "depends_on"
            }}
          ],
          "mermaid_mindmap": "mindmap\\n  root(({request.topic}))\\n    concept((Subtopic))"
        }}
        """

        print(f"[DEBUG] Sending prompt to Gemini for topic '{request.topic}'")

        # 2️⃣ Call Gemini
        raw = gemini_client.generate(prompt=prompt)
        print("[DEBUG] Raw Gemini response preview:", raw[:400])

        # 3️⃣ Try parsing JSON
        try:
            payload_str = _extract_json_payload(raw)
            payload = json.loads(payload_str)
            print(f"[DEBUG] ✅ JSON parsed successfully for '{request.topic}'")
        except Exception as e:
            print(f"[WARN] Gemini output invalid, using fallback. Error: {e}")
            payload = _fallback_mindmap(request.topic, request.subject)

        # 4️⃣ Extract fields
        nodes_raw = payload.get("nodes", [])
        edges_raw = payload.get("edges", [])
        mermaid_raw = payload.get("mermaid_mindmap")

        # 5️⃣ If Gemini didn’t give nodes, fallback
        if not nodes_raw:
            print("[WARN] No nodes detected, using fallback mindmap")
            fallback = _fallback_mindmap(request.topic, request.subject)
            nodes_raw = fallback["nodes"]
            edges_raw = fallback["edges"]
            mermaid_raw = fallback["mermaid_mindmap"]

        # 6️⃣ Final response
        response = MindMapResponse(
            nodes=nodes_raw,
            edges=edges_raw,
            topic=request.topic,
            subject=request.subject,
            generated_at=datetime.utcnow().isoformat(),
            mermaid_mindmap=mermaid_raw
        )

        print(f"[SUCCESS] ✅ Mind map generated for topic: {request.topic}")
        return response

    # except Exception as e:
    #     logger.error(f"Error generating mind map: {e}")
    #     # Raise a generic error without exposing sensitive details
    #     raise HTTPException(status_code=500, detail="Mind map generation failed")
    except Exception as e:
        import traceback
        logger.error("❌ Full error traceback:")
        traceback.print_exc()
        logger.error(f"[ERROR] Mind map generation failed: {e}")
        # Raise a generic error without exposing internal details
        raise HTTPException(status_code=500, detail="Mind map generation failed")

@router.get("/topics/suggestions", response_model=Dict[str, Any])
def get_suggestions():
    return {"suggestions": [
        {"topic": "Calculus", "subject": "Math"},
        {"topic": "Organic Chemistry", "subject": "Chemistry"},
        {"topic": "Electricity & Magnetism", "subject": "Physics"}
    ]}















# """
# Mind Map API - AI-powered concept visualization endpoint
# """
# from fastapi import APIRouter, HTTPException, Depends
# from pydantic import BaseModel, Field
# from typing import List, Optional, Dict, Any, Tuple, Set
# import logging
# import json
# import re
# from datetime import datetime

# from app.core.config import settings
# from app.services.llm.gemini_client import GeminiClient
# from app.services.llm.prompts import JEEPromptTemplates

# logger = logging.getLogger(__name__)
# router = APIRouter(prefix="/mindmap", tags=["Mind Map"])


# # Pydantic models
# class MindMapRequest(BaseModel):
#     """Request model for mind map generation."""
#     topic: str = Field(..., min_length=2, max_length=200, description="Topic to generate mind map for")
#     subject: Optional[str] = Field(None, description="Subject filter (Physics, Chemistry, Math)")
#     max_nodes: int = Field(8, ge=3, le=15, description="Maximum number of concept nodes")
#     include_examples: bool = Field(True, description="Include examples in node details")


# class MindMapNode(BaseModel):
#     """A node in the mind map."""
#     id: str
#     label: str
#     summary: str
#     description: str
#     related_concepts: List[str]
#     examples: Optional[List[str]] = None
#     subject: Optional[str] = None
#     difficulty_level: str = Field("intermediate", description="beginner/intermediate/advanced")


# class MindMapEdge(BaseModel):
#     """An edge connecting two nodes."""
#     id: str
#     source: str
#     target: str
#     label: str
#     relationship_type: str = Field("related", description="related/depends_on/prerequisite")


# class MindMapResponse(BaseModel):
#     """Response model for mind map generation."""
#     nodes: List[MindMapNode]
#     edges: List[MindMapEdge]
#     topic: str
#     subject: Optional[str] = None
#     generated_at: str
#     mermaid_mindmap: Optional[str] = None


# # Dependency: Get Gemini client
# def get_gemini_client():
#     """Initialize and return Gemini client."""
#     try:
#         gemini_api_key = getattr(settings, 'GEMINI_API_KEY', None)
#         if not gemini_api_key:
#             # For demo purposes, return a mock client that raises an informative error
#             class MockGeminiClient:
#                 def generate(self, *args, **kwargs):
#                     # Return mock mindmap data for testing
#                     mock_response = '''{
#                         "nodes": [
#                             {
#                                 "id": "polymers_basics",
#                                 "label": "Polymer Basics",
#                                 "summary": "Introduction to polymers and their classification",
#                                 "description": "Polymers are large molecules composed of repeating structural units called monomers. They can be natural or synthetic, and are classified as addition or condensation polymers based on their formation mechanism.",
#                                 "related_concepts": ["monomers", "macromolecules", "addition_polymers"],
#                                 "examples": ["Polyethylene from ethylene monomers", "PVC from vinyl chloride"],
#                                 "subject": "Chemistry",
#                                 "difficulty_level": "intermediate"
#                             },
#                             {
#                                 "id": "addition_polymers",
#                                 "label": "Addition Polymers",
#                                 "summary": "Polymers formed by addition reactions",
#                                 "description": "Addition polymers are formed when unsaturated monomers join together without losing any atoms. The reaction involves opening of double bonds and formation of single bonds.",
#                                 "related_concepts": ["unsaturated_monomers", "free_radical", "polyethylene"],
#                                 "examples": ["Polyethylene (PE)", "Polypropylene (PP)", "PVC"],
#                                 "subject": "Chemistry",
#                                 "difficulty_level": "intermediate"
#                             }
#                         ],
#                         "edges": [
#                             {
#                                 "id": "edge_1",
#                                 "source": "polymers_basics",
#                                 "target": "addition_polymers",
#                                 "label": "includes",
#                                 "relationship_type": "related"
#                             }
#                         ]
#                     }'''
#                     return mock_response
#             return MockGeminiClient()
#         return GeminiClient(api_key=gemini_api_key)
#     except Exception as e:
#         logger.error(f"Failed to initialize Gemini client: {e}")
#         raise HTTPException(
#             status_code=500,
#             detail="AI service unavailable"
#         )


# def _build_response_schema(include_examples: bool) -> Dict[str, Any]:
#     """Return Gemini response schema for a structured mind map."""
#     node_properties = {
#         "id": {"type": "string"},
#         "label": {"type": "string"},
#         "summary": {"type": "string"},
#         "description": {"type": "string"},
#         "related_concepts": {
#             "type": "array",
#             "items": {"type": "string"},
#             "minItems": 1
#         },
#         "subject": {"type": "string", "nullable": True},
#         "difficulty_level": {"type": "string"}
#     }

#     if include_examples:
#         node_properties["examples"] = {
#             "type": "array",
#             "items": {"type": "string"},
#             "minItems": 0,
#             "nullable": True
#         }

#     schema: Dict[str, Any] = {
#         "type": "object",
#         "properties": {
#             "nodes": {
#                 "type": "array",
#                 "items": {"type": "object", "properties": node_properties, "required": list(node_properties.keys())},
#                 "minItems": 3,
#                 "maxItems": 15
#             },
#             "edges": {
#                 "type": "array",
#                 "items": {
#                     "type": "object",
#                     "properties": {
#                         "id": {"type": "string"},
#                         "source": {"type": "string"},
#                         "target": {"type": "string"},
#                         "label": {"type": "string"},
#                         "relationship_type": {"type": "string"}
#                     },
#                     "required": ["id", "source", "target", "label", "relationship_type"]
#                 },
#                 "minItems": 2
#             },
#             "mermaid_mindmap": {"type": "string", "nullable": True}
#         },
#         "required": ["nodes", "edges"]
#     }

#     return schema


# def _sanitize_nodes(nodes: List[Dict[str, Any]], include_examples: bool, max_nodes: int) -> Tuple[List[Dict[str, Any]], Set[str]]:
#     """Clean node data and enforce limits."""
#     cleaned: List[Dict[str, Any]] = []
#     seen_ids: Set[str] = set()

#     for node in nodes:
#         node_id = str(node.get("id", "")).strip()
#         label = str(node.get("label", "")).strip()
#         if not node_id or not label or node_id in seen_ids:
#             continue

#         related = node.get("related_concepts") or []
#         if not isinstance(related, list):
#             related = []

#         clean_node: Dict[str, Any] = {
#             "id": node_id,
#             "label": label,
#             "summary": node.get("summary", "").strip()[:300],
#             "description": node.get("description", "").strip()[:800],
#             "related_concepts": [str(concept).strip() for concept in related if str(concept).strip()],
#             "subject": node.get("subject"),
#             "difficulty_level": (node.get("difficulty_level") or "intermediate").lower()
#         }

#         if include_examples:
#             examples = node.get("examples") or []
#             if isinstance(examples, list):
#                 clean_node["examples"] = [str(example).strip() for example in examples if str(example).strip()][:3]
#             else:
#                 clean_node["examples"] = []

#         cleaned.append(clean_node)
#         seen_ids.add(node_id)

#         if len(cleaned) >= max_nodes:
#             break

#     return cleaned, seen_ids


# def _sanitize_edges(edges: List[Dict[str, Any]], valid_ids: Set[str]) -> List[Dict[str, Any]]:
#     """Keep only edges that reference valid nodes and normalize fields."""
#     cleaned: List[Dict[str, Any]] = []
#     for edge in edges:
#         source = edge.get("source")
#         target = edge.get("target")
#         edge_id = edge.get("id") or f"{source}_{target}"

#         if not source or not target or source not in valid_ids or target not in valid_ids:
#             continue

#         cleaned.append({
#             "id": str(edge_id),
#             "source": str(source),
#             "target": str(target),
#             "label": edge.get("label", "related"),
#             "relationship_type": edge.get("relationship_type", "related")
#         })

#     # Remove duplicate edges based on source-target
#     unique = {}
#     for edge in cleaned:
#         key = (edge["source"], edge["target"])  # direction matters
#         unique[key] = edge

#     return list(unique.values())


# def _fallback_mindmap(topic: str, subject: Optional[str]) -> Dict[str, Any]:
#     """Provide a deterministic fallback mind map if AI generation fails."""
#     root_id = topic.lower().replace(" ", "_") or "core_topic"
#     nodes = [
#         {
#             "id": root_id,
#             "label": topic.title(),
#             "summary": f"Overview of {topic} for JEE preparation.",
#             "description": f"{topic.title()} is a foundational concept. Use this map as a starting point to explore subtopics.",
#             "related_concepts": ["fundamentals", "applications", "common_mistakes"],
#             "examples": [],
#             "subject": subject,
#             "difficulty_level": "intermediate"
#         },
#         {
#             "id": f"{root_id}_fundamentals",
#             "label": f"{topic.title()} Basics",
#             "summary": "Key definitions and core principles.",
#             "description": "Review the fundamental laws, formulas, and conceptual underpinnings.",
#             "related_concepts": ["key_formulas", "core_theorems"],
#             "examples": [],
#             "subject": subject,
#             "difficulty_level": "beginner"
#         },
#         {
#             "id": f"{root_id}_applications",
#             "label": "Applications",
#             "summary": "Typical problems and real-world scenarios.",
#             "description": "Understand how the concept appears in JEE problems and real contexts.",
#             "related_concepts": ["problem_strategies", "jee_patterns"],
#             "examples": [],
#             "subject": subject,
#             "difficulty_level": "intermediate"
#         },
#         {
#             "id": f"{root_id}_common_mistakes",
#             "label": "Common Mistakes",
#             "summary": "Frequent errors students make.",
#             "description": "Watch out for misconceptions and calculation pitfalls.",
#             "related_concepts": ["revision_tips"],
#             "examples": [],
#             "subject": subject,
#             "difficulty_level": "beginner"
#         }
#     ]

#     edges = [
#         {"id": f"{root_id}_to_basics", "source": root_id, "target": f"{root_id}_fundamentals", "label": "includes", "relationship_type": "prerequisite"},
#         {"id": f"{root_id}_to_applications", "source": root_id, "target": f"{root_id}_applications", "label": "leads_to", "relationship_type": "depends_on"},
#         {"id": f"{root_id}_to_mistakes", "source": root_id, "target": f"{root_id}_common_mistakes", "label": "avoid", "relationship_type": "related"}
#     ]

#     mermaid = f"""mindmap
#   root(({topic.title()}))
#     fundamentals((Fundamentals))
#       basics(Key formulas)
#       theorems(Core theorems)
#     applications((Applications))
#       problems(JEE problem types)
#       context(Real-world links)
#     mistakes((Common Mistakes))
#       careless(Calculation slips)
#       concepts(Conceptual gaps)
# """

#     return {"nodes": nodes, "edges": edges, "mermaid_mindmap": mermaid}


# def _extract_json_payload(raw: str) -> str:
#     """Attempt to extract JSON object from raw Gemini response."""
#     if not raw:
#         raise ValueError("Empty response from Gemini")

#     raw = raw.strip()
#     if raw.startswith("{") and raw.endswith("}"):
#         return raw

#     match = re.search(r"\{.*\}", raw, re.DOTALL)
#     if match:
#         return match.group()

#     raise ValueError("Could not find JSON object in response")


# @router.post("/generate", response_model=MindMapResponse)
# def generate_mindmap(
#     request: MindMapRequest,
#     gemini_client: GeminiClient = Depends(get_gemini_client)
# ):
#     """
#     Generate an interactive mind map for a given topic.

#     Uses AI to create concept nodes with relationships, summaries,
#     and examples for visual learning.
#     """
#     try:
#         response_schema = _build_response_schema(request.include_examples)

#         prompt = f"""
# You are an expert JEE tutor who designs structured mind maps.

# Topic: "{request.topic}"
# Subject context: {request.subject or "General JEE"}

# Generate up to {request.max_nodes} highly relevant concept nodes. Start from fundamentals and progressively go to advanced subtopics. Provide concise, exam-focused details.

# Requirements for each node:
# - id: lowercase with underscores only (e.g., kinetic_energy_basics)
# - label: 2-5 word title
# - summary: 1 sentence overview
# - description: 2-4 sentences with JEE-specific insight
# - related_concepts: 3-5 short concept names
# - difficulty_level: beginner, intermediate, or advanced
# {"- examples: Add 2-3 practical or problem-based examples" if request.include_examples else ""}

# Create meaningful edges connecting the nodes. Label each edge with the relationship (related, depends_on, prerequisite, application_of, builds_on).

# Also provide a concise Mermaid mindmap representation in the field "mermaid_mindmap" using the syntax:
# mindmap
#   root(({request.topic.title()}))
#     subtopic(Subtopic label)
#     subtopic2(Subtopic label)

# Return ONLY JSON matching the provided schema.
# """

#         raw_response = gemini_client.generate_json(
#             prompt=prompt,
#             response_schema=response_schema
#         )

#         try:
#             mindmap_payload = json.loads(_extract_json_payload(raw_response))
#         except Exception as parse_error:
#             logger.error("Mindmap JSON parsing failed: %s", parse_error)
#             mindmap_payload = _fallback_mindmap(request.topic, request.subject)

#         nodes_raw = mindmap_payload.get("nodes", [])
#         edges_raw = mindmap_payload.get("edges", [])
#         mermaid_raw = mindmap_payload.get("mermaid_mindmap")

#         nodes_clean, valid_ids = _sanitize_nodes(nodes_raw, request.include_examples, request.max_nodes)
#         edges_clean = _sanitize_edges(edges_raw, valid_ids)

#         if len(nodes_clean) < 3:
#             logger.warning("Insufficient nodes after sanitization, using fallback mind map")
#             fallback = _fallback_mindmap(request.topic, request.subject)
#             nodes_clean, valid_ids = _sanitize_nodes(
#                 fallback["nodes"],
#                 request.include_examples,
#                 request.max_nodes
#             )
#             edges_clean = _sanitize_edges(fallback["edges"], valid_ids)
#             mermaid_raw = fallback.get("mermaid_mindmap")

#         generated_at = datetime.utcnow().isoformat()

#         response_data = MindMapResponse(
#             nodes=nodes_clean,
#             edges=edges_clean,
#             topic=request.topic,
#             subject=request.subject,
#             generated_at=generated_at,
#             mermaid_mindmap=mermaid_raw
#         )

#         logger.info(
#             "Generated mind map for topic '%s' with %d nodes and %d edges",
#             request.topic,
#             len(response_data.nodes),
#             len(response_data.edges)
#         )
#         return response_data

#     except HTTPException:
#         raise

#     except Exception as e:
#         logger.error(f"Error generating mind map: {e}")
#         raise HTTPException(
#             status_code=500,
#             detail=f"Failed to generate mind map: {str(e)}"
#         )


# @router.get("/topics/suggestions")
# async def get_topic_suggestions():
#     """
#     Get suggested topics for mind map generation.
#     Returns popular JEE topics that work well for visual learning.
#     """
#     suggestions = [
#         # Physics
#         {"topic": "Mechanics", "subject": "Physics", "description": "Motion, forces, energy, momentum"},
#         {"topic": "Electricity and Magnetism", "subject": "Physics", "description": "Circuits, fields, electromagnetic waves"},
#         {"topic": "Optics", "subject": "Physics", "description": "Light, lenses, interference, diffraction"},
#         {"topic": "Modern Physics", "subject": "Physics", "description": "Quantum mechanics, relativity, nuclear physics"},

#         # Chemistry
#         {"topic": "Organic Chemistry", "subject": "Chemistry", "description": "Hydrocarbons, functional groups, reactions"},
#         {"topic": "Inorganic Chemistry", "subject": "Chemistry", "description": "Periodic table, coordination compounds, metallurgy"},
#         {"topic": "Physical Chemistry", "subject": "Chemistry", "description": "Thermodynamics, kinetics, electrochemistry"},
#         {"topic": "Polymers", "subject": "Chemistry", "description": "Polymerization, types, properties, applications"},

#         # Mathematics
#         {"topic": "Calculus", "subject": "Math", "description": "Limits, derivatives, integrals, applications"},
#         {"topic": "Coordinate Geometry", "subject": "Math", "description": "Lines, circles, conics, transformations"},
#         {"topic": "Algebra", "subject": "Math", "description": "Complex numbers, matrices, inequalities"},
#         {"topic": "Trigonometry", "subject": "Math", "description": "Identities, equations, properties"}
#     ]

#     return {"suggestions": suggestions}