# RL-Based Personalized Educational Tutor 🎓🤖

> **B.Tech CS AIML and IoT 3rd Year Mini Project**
>
> **Developed by:**
> - **Sanskar Khandelwal**
> - **Krishna Mittal**
> - **Ayush Saroj**

---

## 🎯 Project Overview

The **RL-Tutor-Project** is an advanced, personalized educational platform that leverages **Reinforcement Learning (RL)**, **Generative AI (GenAI)**, and **Machine Learning (ML)** to optimize the learning experience for students. Unlike traditional Learning Management Systems (LMS) that offer static content, this system dynamically adapts to each student's learning pace, style, and knowledge gaps in real-time.

By integrating a **Deep Knowledge Tracing (DKT)** model with a **Proximal Policy Optimization (PPO)** agent, the system acts as an intelligent tutor that selects the most appropriate questions and content to maximize learning gains. Additionally, it features an AI-powered **Doubt Solver** using **Retrieval-Augmented Generation (RAG)** and a **Multi-Armed Bandit** system for content type optimization.

## 🌟 Key Features

- 🧠 **Adaptive Quiz System:** An RL agent (PPO) selects questions based on student history to keep them in the \"Zone of Proximal Development\".
- 🤖 **AI Doubt Solver:** A RAG-based chat interface that answers academic queries with citations from valid study materials (NCERT/JEE).
- 📊 **Smart Recommendations:** Uses Multi-Armed Bandit algorithms to suggest the best content format (Video, Text, Interactive) for each student.
- 🃏 **AI Flashcards:** Generative AI creates personalized flashcards for spaced repetition and revision.
- 📈 **Real-time Knowledge Tracking:** Deep Knowledge Tracing (DKT) estimates mastery of various skills continuously.
- 🎨 **Modern UI:** A beautiful, responsive interface built with Next.js and Aceternity UI.
- 🔐 **Secure Authentication:** JWT-based auth with refresh tokens.

## 🛠️ Tech Stack

### Frontend
- **Framework:** Next.js 14 (React)
- **Language:** TypeScript
- **Styling:** Tailwind CSS, Framer Motion
- **Visualization:** Recharts, React-Flow

### Backend
- **Framework:** FastAPI (Python)
- **Database:** SQLite (Dev) / PostgreSQL (Prod), MongoDB (Vector Store)
- **ORM:** SQLAlchemy, Pydantic

### AI & Machine Learning
- **Reinforcement Learning:** Stable Baselines3 (PPO), Gymnasium
- **Generative AI:** Google Gemini Pro & Flash (via `google-genai` SDK)
- **Knowledge Tracing:** TensorFlow/Keras (LSTM-based DKT)
- **Embeddings:** `text-embedding-004`

## 🏗️ System Architecture

### High-Level Architecture
\`\`\`mermaid
graph TD
    User[Student] -->|HTTPS| FE[Next.js Frontend]
    FE -->|REST API| BE[FastAPI Backend]
    
    subgraph Backend Services
        BE --> Auth[Auth Service]
        BE --> RL[RL Engine (PPO/DKT)]
        BE --> MAB[Bandit Service]
        BE --> RAG[RAG Service]
    end
    
    subgraph Data Layer
        BE --> SQL[(Relational DB)]
        RAG --> Vector[(Vector DB)]
    end
    
    subgraph External AI
        RAG --> Gemini[Google Gemini API]
        RL --> Gemini
    end
\`\`\`

### RL Training Loop
\`\`\`mermaid
sequenceDiagram
    participant Agent as PPO Teacher Agent
    participant Env as Question Environment
    participant Student as Student Model (DKT)
    
    loop Training Step
        Agent->>Env: Select Action (Question ID)
        Env->>Student: Simulate Student Answer
        Student-->>Env: Return Correctness & New State
        Env->>Env: Calculate Reward
        Env-->>Agent: Next State, Reward
        Agent->>Agent: Update Policy
    end
\`\`\`

## 🔬 Methodology

### 1. Reinforcement Learning (Teacher Agent)
- **Algorithm:** Proximal Policy Optimization (PPO)
- **Goal:** Select the next question to maximize learning improvement.
- **Reward Function:** Balances *Improvement* (learning gain), *Answerability* (avoiding frustration), and *Coverage* (addressing weak skills).

### 2. Multi-Armed Bandit (Content Optimization)
- **Algorithm:** Epsilon-Greedy
- **Goal:** Discover the best content format (Video vs. Text) for the user.
- **Mechanism:** Explores new formats occasionally ($\epsilon$) while exploiting the best-performing format most of the time.

### 3. Retrieval-Augmented Generation (Doubt Solver)
- **Process:** Embeds student queries, retrieves relevant chunks from the vector database (MongoDB), and uses Gemini to generate an accurate, cited answer.

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- Python 3.8+
- npm or yarn

### 1. Frontend (Next.js)

\`\`\`bash
# Install dependencies
npm install

# Run development server
npm run dev
\`\`\`

Visit: **http://localhost:3000**

### 2. Backend (FastAPI)

\`\`\`bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Seed database
python seed_db.py

# Run server
python -m uvicorn main:app --host 0.0.0.0 --port 8002 --reload
\`\`\`

Visit: **http://localhost:8002/docs** (API Documentation)

## 📁 Project Structure

\`\`\`
mini_project/
├── app/                      # Next.js Frontend
│   ├── components/          # UI Components (Chat, Flashcards, etc.)
│   ├── app/                 # App Router Pages
│   └── lib/                 # Utilities
├── backend/                 # FastAPI Backend
│   ├── app/
│   │   ├── api/            # API endpoints (Smart Recommendations, Doubt Solver)
│   │   ├── core/           # Configuration
│   │   ├── models/         # Database models
│   │   └── services/       # RL Agent, RAG, & Gemini Client
│   ├── main.py             # FastAPI app entry point
│   └── seed_db.py          # Database seeding script
├── personalized_learning_rl/ # RL Training & Environment
│   ├── agents/             # PPO Agent Code
│   ├── environment/        # Custom Gym Environment
│   └── models/             # Trained DKT Models
├── PROJECT_REPORT.md       # Detailed Project Report
└── README.md              # This file
\`\`\`
'''
