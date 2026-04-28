# 🤖 Task Automation Agent

> An autonomous AI agent with **human-in-the-loop approval** — proposes a plan, waits for your review, then executes tools step by step.

[![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com)
[![Live Demo](https://img.shields.io/badge/Live%20Demo-Render-purple?style=flat-square)](https://task-automation-agent-4.onrender.com)

## 🌐 Live Demo
**→ https://task-automation-agent-4.onrender.com**

Interactive API Docs → https://task-automation-agent-4.onrender.com/docs

---

## 📌 What It Does

1. **User submits a task** in natural language
2. **Agent generates a plan** — breaks it into steps mapped to tools
3. **Human reviews and approves** — toggle steps on/off before execution
4. **Agent executes approved steps** — runs tools and returns results

---

## 🛠️ Tools Available

| Tool | Description |
|------|-------------|
| `web_search` | Search the web for information |
| `summarize_text` | Condense long text to bullet points |
| `create_file` | Write results to a file |
| `calculate` | Safely evaluate math expressions |
| `fetch_weather` | Get weather for a city |
| `send_email_draft` | Draft an email (no actual send) |

---

## 🧠 AI/ML Concepts Demonstrated

- **Agentic AI** — autonomous task decomposition and execution
- **Human-in-the-Loop (HITL)** — human approval before any action
- **Tool Use / Function Calling** — agent mapped to discrete executable tools
- **Safety by Design** — no action without explicit approval

---

## 👤 Author

**Mohammed Inabah Khan**
- [LinkedIn](https://www.linkedin.com/in/mohammed-inabah-khan-0696ba3a5)
- [GitHub](https://github.com/inabahk)
