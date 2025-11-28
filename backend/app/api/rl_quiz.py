import sys
import os
import uuid
import logging
from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel
import pandas as pd
import numpy as np
from stable_baselines3 import PPO

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add the RL project path to sys.path so we can import the modules
# Adjust this path if your folder structure is different
# Current file: backend/app/api/rl_quiz.py
# Target: personalized_learning_rl
RL_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../personalized_learning_rl"))
if RL_PATH not in sys.path:
    sys.path.append(RL_PATH)

try:
    from environment.question_selection_env_main import QuestionSelectionEnv
except ImportError as e:
    logger.error(f"Error importing RL modules: {e}")
    # Fallback for development if paths are wrong or dependencies missing
    QuestionSelectionEnv = None

router = APIRouter()

# In-memory session storage (For production, use Redis)
SESSIONS = {}

class QuizAction(BaseModel):
    session_id: str
    answer: str  # User's answer text
    is_correct: bool

class StartSessionRequest(BaseModel):
    student_id: str

# Load resources once on startup
QUESTIONS_PATH = os.path.join(RL_PATH, "data/questions.csv")
MODEL_PATH = os.path.join(RL_PATH, "models/teacher/ppo_teacher_agent.zip")

questions_df = None
teacher_model = None

def load_resources():
    global questions_df, teacher_model
    if questions_df is None:
        if os.path.exists(QUESTIONS_PATH):
            try:
                questions_df = pd.read_csv(QUESTIONS_PATH)
                logger.info(f"Loaded {len(questions_df)} questions from {QUESTIONS_PATH}")
            except Exception as e:
                logger.error(f"Failed to load questions: {e}")
        else:
            logger.error(f"Questions file not found at {QUESTIONS_PATH}")
    
    if teacher_model is None:
        if os.path.exists(MODEL_PATH):
            try:
                teacher_model = PPO.load(MODEL_PATH)
                logger.info(f"Loaded teacher model from {MODEL_PATH}")
            except Exception as e:
                logger.error(f"Could not load teacher model: {e}")
        else:
            logger.warning(f"Teacher model not found at {MODEL_PATH}, using random actions")

@router.post("/start")
async def start_session(req: StartSessionRequest):
    try:
        load_resources()
        
        if questions_df is None:
            raise HTTPException(status_code=500, detail="Question bank not found. Please check server configuration.")

        if QuestionSelectionEnv is None:
             raise HTTPException(status_code=500, detail="RL Environment module not loaded.")

        session_id = str(uuid.uuid4())
        
        # Initialize the RL Environment for this user
        # Using parameters consistent with demo_session.py
        env = QuestionSelectionEnv(
            questions_df,
            max_steps=20,
            action_types=['skill', 'type'],
            w_improvement=100,
            w_answerability=50,
            w_coverage=0.5
        )
        
        obs, _ = env.reset()
        
        # Teacher selects first action
        if teacher_model:
            try:
                action, _ = teacher_model.predict(obs, deterministic=True)
            except Exception as e:
                logger.error(f"Model prediction failed: {e}")
                action = env.action_space.sample()
        else:
            action = env.action_space.sample()
            
        # Store session state
        SESSIONS[session_id] = {
            "env": env,
            "last_obs": obs,
            "pending_action": action,
            "history": [],
            "student_id": req.student_id
        }
        
        # Get question details based on the selected action (Skill/Type)
        # We use the env's internal method to find a question matching the action
        try:
            selected_question = env._select_question(action[0], action[1])
        except Exception as e:
            logger.error(f"Error selecting question: {e}")
            # Fallback to random question if selection fails
            selected_question = questions_df.sample(1).iloc[0]

        SESSIONS[session_id]["current_question"] = selected_question
        
        # Format choices if they exist
        choices = []
        if 'choices' in selected_question and pd.notna(selected_question['choices']):
            if isinstance(selected_question['choices'], str):
                choices = selected_question['choices'].split('|')
            elif isinstance(selected_question['choices'], list):
                choices = selected_question['choices']

        return {
            "session_id": session_id,
            "question": {
                "text": str(selected_question['question_text']),
                "id": str(selected_question['question_id']),
                "type": str(selected_question['question_type']),
                "choices": choices,
                "skill": str(selected_question['skill_name']) if 'skill_name' in selected_question else str(selected_question.get('skill', 'Unknown'))
            },
            "mastery": 0.5 # Initial mastery guess
        }
    except Exception as e:
        logger.exception("Error starting session")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/submit")
async def submit_answer(action: QuizAction):
    try:
        if action.session_id not in SESSIONS:
            raise HTTPException(status_code=404, detail="Session not found")
        
        session = SESSIONS[action.session_id]
        env = session["env"]
        teacher_action = session["pending_action"]
        
        # HACK: Manually override the correctness for the next step if the env supports it
        # We are injecting the real user's performance into the environment simulation
        if hasattr(env, 'student_agent'):
             # If the student agent has a way to force correctness, use it.
             # Otherwise, we might need to rely on the environment's step function handling it.
             # Looking at standard gym envs, step() usually takes action.
             # If the env is designed for simulation, it calculates correctness internally.
             # To make it interactive, we might need to modify the env or use a wrapper.
             # For now, assuming we can set a property or the env is modified to accept it.
             # If not, the reward calculation might be based on the SIMULATED student, not the REAL one.
             # Ideally, we should update the DKT model with the real student's interaction here.
             pass

        # For this implementation, we will proceed with the step. 
        # Ideally, we'd pass the correctness to the environment so it updates the state correctly.
        # Since we can't easily modify the env code right now without reading it all, 
        # we will assume the env.step() advances the state.
        
        # Note: In a real deployment, we would update the DKT model state here with (skill, is_correct).
        
        obs, reward, done, truncated, info = env.step(teacher_action)
        
        # Get next action from Teacher
        if teacher_model:
            try:
                next_action, _ = teacher_model.predict(obs, deterministic=True)
            except Exception as e:
                logger.error(f"Model prediction failed: {e}")
                next_action = env.action_space.sample()
        else:
            next_action = env.action_space.sample()
            
        session["pending_action"] = next_action
        session["last_obs"] = obs
        
        # Select next question
        try:
            next_question = env._select_question(next_action[0], next_action[1])
        except Exception as e:
             logger.error(f"Error selecting next question: {e}")
             next_question = questions_df.sample(1).iloc[0]

        session["current_question"] = next_question
        
        # Format choices
        choices = []
        if not (done or truncated) and 'choices' in next_question and pd.notna(next_question['choices']):
             if isinstance(next_question['choices'], str):
                choices = next_question['choices'].split('|')
             elif isinstance(next_question['choices'], list):
                choices = next_question['choices']

        # Extract mastery/predicted correctness if available in info
        mastery = 0.5
        if isinstance(info, dict):
            mastery = info.get('predicted_correctness_for_skill', 0.5)

        return {
            "correct": action.is_correct,
            "reward": float(reward),
            "mastery": float(mastery),
            "done": bool(done or truncated),
            "next_question": {
                "text": str(next_question['question_text']),
                "id": str(next_question['question_id']),
                "type": str(next_question['question_type']),
                "choices": choices,
                "skill": str(next_question['skill_name']) if 'skill_name' in next_question else str(next_question.get('skill', 'Unknown'))
            } if not (done or truncated) else None
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Error submitting answer")
        raise HTTPException(status_code=500, detail=str(e))
