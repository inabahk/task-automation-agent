# 🤖 Task Automation Agent

> An autonomous AI agent with **human-in-the-loop approval** — proposes a plan, waits for your review, then executes tools step by step.

[![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)

---

## 📌 What It Does

1. **User submits a task** in natural language — e.g. *"Search for AI trends and save a summary"*
2. **Agent generates a plan** — breaks the task into steps mapped to specific tools
3. **Human reviews and approves** — toggle individual steps on/off before execution
4. **Agent executes approved steps** — runs tools and returns results in real time

This demonstrates the core principle of **safe agentic AI**: the agent proposes, the human controls.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend (HTML/JS)                   │
│  Task Input → Plan Review → Step Toggles → Results View     │
└───────────────────────┬─────────────────────────────────────┘
                        │ REST API calls
┌───────────────────────▼─────────────────────────────────────┐
│                  FastAPI Backend (Python)                    │
│                                                             │
│  POST /plan    → generate_plan(task)  → session created     │
│  POST /approve → record approved steps                      │
│  POST /execute → run tools, return results                  │
└───────────────────────┬─────────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────────┐
│                    Agent Core (agent.py)                    │
│                                                             │
│  TaskAgent                                                  │
│  ├── generate_plan()   — keyword NLP → tool selection       │
│  ├── approve_plan()    — record human decision              │
│  └── execute_session() — run tools, collect results         │
│                                                             │
│  Tools: web_search | summarize_text | create_file           │
│         send_email_draft | calculate | fetch_weather        │
│         list_files                                          │
└─────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tools Available

| Tool | Description | Risk |
|------|-------------|------|
| `web_search` | Search the web for information | Low |
| `summarize_text` | Condense long text to bullet points | Low |
| `create_file` | Write results to a file | Low |
| `calculate` | Safely evaluate math expressions | Low |
| `fetch_weather` | Get weather for a city | Low |
| `send_email_draft` | Draft an email (no actual send) | Medium |
| `list_files` | List files in the output directory | Low |

---

## 🚀 Running Locally

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/task-automation-agent.git
cd task-automation-agent
```

### 2. Install dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 3. Start the server
```bash
uvicorn app:app --reload --port 8000
```

### 4. Open the UI
Open `frontend/index.html` in your browser **or** visit:
```
http://localhost:8000
```

### 5. Try the API directly
```
http://localhost:8000/docs   ← Interactive Swagger UI
```

---

## 🌐 Deployment

### Backend → Render.com (Free)
1. Push this repo to GitHub
2. Go to [render.com](https://render.com) → New → Web Service
3. Connect your repo — Render auto-detects `render.yaml`
4. Deploy! You'll get a public URL like `https://task-agent-xyz.onrender.com`

### Frontend → GitHub Pages (Free)
1. Go to your repo Settings → Pages
2. Set source to `main` branch, `/frontend` folder
3. Done — live at `https://YOUR_USERNAME.github.io/task-automation-agent`

**Update the API URL** in `frontend/index.html`:
```js
const API = 'https://your-render-url.onrender.com';
```

---

## 📡 API Reference

### `POST /plan`
Submit a task and get a proposed execution plan.
```json
{ "task": "Search for AI trends and save a summary file" }
```
**Response:** session ID + list of steps

### `POST /approve`
Approve specific steps (human-in-the-loop).
```json
{ "session_id": "abc-123", "approved_steps": [1, 2, 3] }
```

### `POST /execute/{session_id}`
Execute the approved steps and get results.

### `GET /session/{session_id}`
Get full session state.

### `GET /tools`
List all available tools.

---

## 🔮 Extending This Project

To connect real tools, replace the simulated responses in `agent.py`:

```python
# Real web search (SerpAPI)
import serpapi
results = serpapi.search({"q": query, "api_key": os.getenv("SERPAPI_KEY")})

# Real LLM-powered planning (Anthropic)
import anthropic
client = anthropic.Anthropic()
message = client.messages.create(model="claude-opus-4-5", ...)

# Real weather (OpenWeatherMap)
import requests
resp = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}")
```

---

## 🧠 AI/ML Concepts Demonstrated

- **Agentic AI** — autonomous task decomposition and execution
- **Human-in-the-Loop (HITL)** — human approval before any action
- **Tool Use / Function Calling** — agent mapped to discrete executable tools
- **Session State Management** — stateful multi-step workflows
- **Safety by Design** — no action without explicit approval

---

## 📂 Project Structure

```
task-automation-agent/
├── backend/
│   ├── agent.py         ← Core agent: plan + execute logic
│   ├── app.py           ← FastAPI REST API
│   └── requirements.txt
├── frontend/
│   └── index.html       ← UI (no framework, pure HTML/CSS/JS)
├── render.yaml          ← Render.com deployment config
├── Procfile             ← Heroku/Railway deployment
└── README.md
```

---

## 👤 Author

**Mohammed Inabah Khan**
- BTech Student | AI/ML Enthusiast
- [LinkedIn](https://www.linkedin.com/in/mohammed-inabah-khan-0696ba3a5)
- [GitHub](https://github.com/inabahk)

---

## 📄 License

MIT — free to use, modify, and deploy.
