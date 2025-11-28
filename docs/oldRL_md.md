A reinforcement learning framework for adaptive tutoring that combines Deep Knowledge Tracing (DKT) with a PPO teacher policy to deliver the next best question for each learner. The project ships with diagnostics, reproducible training scripts, pretrained student models, and a Flask demo app that showcases the end-to-end personalized quiz experience.

---

## Highlights

- **Curriculum Intelligence:** PPO-based teacher agent trained to maximize mastery gains, coverage of weak skills, and question answerability.
- **Student Modeling:** LSTM DKT network (`models/dkt_model_working.keras`) that predicts per-skill mastery vectors from historical interactions.
- **Rich Question Bank:** 1,000+ items tagged by skill, difficulty, and modality (`data/questions.csv`) sourced from Assistments and curated datasets.
- **Transparent Evaluation:** Comprehensive diagnostics (`diagnostic.py`) and pipeline tests (`test_rl_pipeline.py`) for quick health checks.
- **Interactive Demo:** `app.py` exposes a lightweight adaptive quiz web UI backed by the RL environment and optional PPO policy.

---

## Repository Layout

| Path | Description |
| --- | --- |
| `agents/` | Notebooks and scripts for student/teacher agents (DKT, PPO training experiments). |
| `environment/` | `QuestionSelectionEnv` Gymnasium environment that orchestrates question selection, scoring, and history logging. |
| `models/` | Pretrained DKT weights plus space for exported PPO policies (`models/teacher/ppo_policy.zip`). |
| `trainings/` | TensorBoard logs, history JSON traces, and PPO rollout artifacts. |
| `data/` | Question bank (`questions.csv`), cleaned Assistments data, curriculum skill taxonomy. |
| `plots/` | Visualizations and analysis results. |
| `demo_session.py` | CLI demo for stepping through a learning session. |
| `app.py` | Flask adaptive quiz application. |

---

## Quick Start

> Requires Python 3.9 (TensorFlow 2.10 constraint) and a virtual environment.

```bash
git clone https://github.com/somtee99/personalized_learning_rl.git
cd personalized_learning_rl
python -m venv venv_rl
venv_rl\Scripts\activate  # on Windows (use source venv_rl/bin/activate on Unix)
pip install --upgrade pip
pip install -r requirements.txt
```

Populate the `data/` directory with:
- `questions.csv` (already included) – ensure custom edits preserve the header: `id,question_text,answer,skill,difficulty,question_type,choices`
- `assistments_dataset.csv` (optional; only needed for raw data experiments)

---

## Running Diagnostics & Tests

```bash
# 1. Full project diagnostic (checks data, models, env, dependencies)
python diagnostic.py

# 2. End-to-end RL pipeline test (loads DKT, spins env, trains PPO for a few steps)
python test_rl_pipeline.py
```

Typical success output shows model loading, environment initialization, PPO training, and interaction loop completion with adaptive question logs.

---

## Training & Saving a PPO Teacher

1. Configure your PPO training script or notebook (see `trainings/` history json for prior runs).
2. After training, export the policy for inference:
   ```python
   ppo.save("models/teacher/ppo_policy.zip")
   ```
3. The demo app will automatically load the policy when present; otherwise it falls back to a weakest-skill heuristic.

---

## Launching the Adaptive Quiz Demo

```bash
python app.py
# visit http://127.0.0.1:5000/
```

Each session instantiates `QuestionSelectionEnv`, optionally queries the PPO policy for an action, and renders the next question with multiple-choice or free-response UI. The summary page surfaces accuracy, rewards, and a table of interactions. Sessions remain in memory; restart the app or `POST /reset/<session_id>` to clear.

---

## Architecture Overview

```
┌───────────────────────────────┐         observe + reward
│   PPO Teacher (Stable-Baselines3)│◀────────────────┐
│  • Maximizes mastery & coverage │                 │
└───────────────▲────────────────┘                 │
                │ action (skill, type)             │
┌───────────────┴────────────────┐    mastery vector│
│ QuestionSelectionEnv (Gymnasium)│─────────────────┤
│ • Encodes question metadata      │                 │
│ • Computes reward + logging      │                 │
└───────────────▲────────────────┘                 │
                │ predictions                       │
┌───────────────┴────────────────┐                 │
│   DKT Student Model (Keras)     │                 │
│ • LSTM knowledge tracing        │                 │
└───────────────▲────────────────┘                 │
                │ history / answers                │
┌───────────────┴────────────────┐                 │
│ Question Bank + Skill Taxonomy │─────────────────┘
│ • Tagged by topic / difficulty  │
└────────────────────────────────┘
```

Reward signal is a weighted combination of mastery improvement, question answerability, and weak-skill coverage. All interactions are logged to `trainings/history/history.json` for later analysis.

---

## Datasets & Models

- **Question bank:** `data/questions.csv` (skills, difficulty, type, optional choices).
- **Cleaned interaction data:** `data/cleaned_df.csv` for DKT training.
- **Curriculum skills:** `curriculum_skills.json` enumerates 174 skill labels.
- **Pretrained DKT:** `models/dkt_model_working.keras` (sequence-to-mastery predictor).
- **Optional assets:** Additional `.keras`, `.h5`, and TensorFlow checkpoints retained for experimentation.

---

## Notebooks & Experiments

- `agents/student_lstm_agent_kt-skill.ipynb` – DKT training and evaluation.
- `agents/student_lstm_agent_kt-skill+qt.ipynb` – DKT with question type augmentations.
- `data_cleaning.ipynb`, `plotting.ipynb` – Data preparation and exploratory plots.

Each notebook includes markdown guidance and requires the environment setup above.

---

## Roadmap Ideas

- Persist user sessions with SQLite or Supabase for longitudinal tracking.
- Extend reward function with latency or engagement metrics.
- Add teacher dashboard for cohort-level analytics.
- Deploy the Flask app with gunicorn/uvicorn and enable OAuth for real students.

---

## Contributing & Support

1. Fork and create a feature branch (`git checkout -b feature/my-feature`).
2. Run diagnostics/tests before opening a PR.
3. Submit pull requests with a summary, screenshots/logs when relevant, and testing notes.

Bug reports and feature requests are welcome via GitHub Issues. For discussions or collaboration, open an issue or reach out to the maintainers.

