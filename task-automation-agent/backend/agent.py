"""
Task Automation Agent - Core Logic
===================================
An AI agent that:
1. Receives a task from the user
2. Breaks it into a plan of steps
3. Waits for human approval (human-in-the-loop)
4. Executes approved tools step by step
5. Returns results
"""

import json
import datetime
import os
import re
from typing import Any

# ──────────────────────────────────────────
# TOOL DEFINITIONS
# ──────────────────────────────────────────

TOOLS = {
    "web_search": {
        "description": "Searches the web for information on a given query.",
        "parameters": {"query": "string"},
    },
    "summarize_text": {
        "description": "Summarizes a long piece of text into key bullet points.",
        "parameters": {"text": "string"},
    },
    "create_file": {
        "description": "Creates a text file with the given content.",
        "parameters": {"filename": "string", "content": "string"},
    },
    "send_email_draft": {
        "description": "Drafts an email with subject and body (does NOT send — safe preview only).",
        "parameters": {"to": "string", "subject": "string", "body": "string"},
    },
    "calculate": {
        "description": "Evaluates a safe mathematical expression and returns the result.",
        "parameters": {"expression": "string"},
    },
    "fetch_weather": {
        "description": "Fetches current weather for a given city.",
        "parameters": {"city": "string"},
    },
    "list_files": {
        "description": "Lists files in the output directory.",
        "parameters": {},
    },
}


# ──────────────────────────────────────────
# TOOL EXECUTOR (Simulated / Safe)
# ──────────────────────────────────────────

def execute_tool(tool_name: str, params: dict) -> dict:
    """Execute a tool and return its result."""
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")

    if tool_name == "web_search":
        query = params.get("query", "")
        # Simulated search results (in production, use SerpAPI / Brave Search API)
        return {
            "status": "success",
            "tool": tool_name,
            "result": (
                f"[Simulated Web Search for: '{query}']\n"
                f"• Result 1: Overview of '{query}' — Wikipedia\n"
                f"• Result 2: Recent developments in '{query}' — TechCrunch\n"
                f"• Result 3: How '{query}' works — Medium\n"
                f"(In production, connect SerpAPI or Brave Search for real results.)"
            ),
            "timestamp": timestamp,
        }

    elif tool_name == "summarize_text":
        text = params.get("text", "")
        words = text.split()
        preview = " ".join(words[:20]) + ("..." if len(words) > 20 else "")
        return {
            "status": "success",
            "tool": tool_name,
            "result": (
                f"Summary of provided text ({len(words)} words):\n"
                f"• Key point 1: {preview}\n"
                f"• Key point 2: The text discusses relevant concepts in depth.\n"
                f"• Key point 3: Conclusion relates to the main topic."
            ),
            "timestamp": timestamp,
        }

    elif tool_name == "create_file":
        filename = params.get("filename", "output.txt")
        content = params.get("content", "")
        # Sanitize filename
        filename = re.sub(r"[^\w\-_\. ]", "_", filename)
        os.makedirs("outputs", exist_ok=True)
        filepath = os.path.join("outputs", filename)
        with open(filepath, "w") as f:
            f.write(content)
        return {
            "status": "success",
            "tool": tool_name,
            "result": f"File '{filename}' created successfully with {len(content)} characters.",
            "timestamp": timestamp,
        }

    elif tool_name == "send_email_draft":
        to = params.get("to", "")
        subject = params.get("subject", "")
        body = params.get("body", "")
        return {
            "status": "success",
            "tool": tool_name,
            "result": (
                f"📧 Email Draft Created (NOT sent):\n"
                f"To: {to}\n"
                f"Subject: {subject}\n"
                f"Body:\n{body}"
            ),
            "timestamp": timestamp,
        }

    elif tool_name == "calculate":
        expression = params.get("expression", "")
        # Safe eval: only allow math characters
        safe_expr = re.sub(r"[^\d\+\-\*\/\.\(\)\s\%]", "", expression)
        try:
            result = eval(safe_expr, {"__builtins__": {}})
            return {
                "status": "success",
                "tool": tool_name,
                "result": f"{expression} = {result}",
                "timestamp": timestamp,
            }
        except Exception as e:
            return {
                "status": "error",
                "tool": tool_name,
                "result": f"Could not evaluate expression: {expression}. Error: {str(e)}",
                "timestamp": timestamp,
            }

    elif tool_name == "fetch_weather":
        city = params.get("city", "")
        # Simulated weather (connect OpenWeatherMap API in production)
        return {
            "status": "success",
            "tool": tool_name,
            "result": (
                f"[Simulated Weather for {city}]\n"
                f"🌤 Partly Cloudy | 28°C | Humidity: 62%\n"
                f"Wind: 14 km/h NE | Feels like: 30°C\n"
                f"(Connect OpenWeatherMap API for real data.)"
            ),
            "timestamp": timestamp,
        }

    elif tool_name == "list_files":
        os.makedirs("outputs", exist_ok=True)
        files = os.listdir("outputs")
        if files:
            file_list = "\n".join(f"• {f}" for f in files)
        else:
            file_list = "(No files yet — create_file tool will place files here.)"
        return {
            "status": "success",
            "tool": tool_name,
            "result": f"Files in outputs/:\n{file_list}",
            "timestamp": timestamp,
        }

    else:
        return {
            "status": "error",
            "tool": tool_name,
            "result": f"Unknown tool: '{tool_name}'",
            "timestamp": timestamp,
        }


# ──────────────────────────────────────────
# PLAN GENERATOR (Rule-based + keyword NLP)
# ──────────────────────────────────────────

def generate_plan(task: str) -> list[dict]:
    """
    Generates a step-by-step plan for the given task.
    In production: replace with LLM call (OpenAI / Claude API).
    """
    task_lower = task.lower()
    plan = []
    step_id = 1

    # Detect intent and map to tools
    if any(w in task_lower for w in ["search", "find", "look up", "research", "what is", "who is"]):
        query = task.replace("search for", "").replace("find", "").replace("look up", "").strip()
        plan.append({
            "step": step_id,
            "tool": "web_search",
            "description": f"Search the web for: {query}",
            "params": {"query": query},
            "risk": "low",
        })
        step_id += 1
        plan.append({
            "step": step_id,
            "tool": "summarize_text",
            "description": "Summarize the search results into key points",
            "params": {"text": f"Search results for: {query}"},
            "risk": "low",
        })
        step_id += 1

    if any(w in task_lower for w in ["weather", "temperature", "forecast", "climate"]):
        # Try to extract city name
        words = task.split()
        city = "Hyderabad"
        for i, w in enumerate(words):
            if w.lower() in ["in", "for", "at"] and i + 1 < len(words):
                city = words[i + 1]
                break
        plan.append({
            "step": step_id,
            "tool": "fetch_weather",
            "description": f"Fetch current weather for {city}",
            "params": {"city": city},
            "risk": "low",
        })
        step_id += 1

    if any(w in task_lower for w in ["calculate", "compute", "math", "sum", "multiply", "divide"]):
        expr = re.sub(r"[^\d\+\-\*\/\.\(\)\s]", "", task)
        if not expr.strip():
            expr = "2 + 2"
        plan.append({
            "step": step_id,
            "tool": "calculate",
            "description": f"Calculate: {expr.strip()}",
            "params": {"expression": expr.strip()},
            "risk": "low",
        })
        step_id += 1

    if any(w in task_lower for w in ["email", "draft", "write to", "message", "send"]):
        plan.append({
            "step": step_id,
            "tool": "send_email_draft",
            "description": "Draft an email based on the task description",
            "params": {
                "to": "recipient@example.com",
                "subject": f"Re: {task[:40]}",
                "body": f"Hi,\n\nI'm writing regarding: {task}\n\nPlease let me know your thoughts.\n\nBest regards",
            },
            "risk": "medium",
        })
        step_id += 1

    if any(w in task_lower for w in ["file", "save", "write", "create", "document", "report", "note"]):
        plan.append({
            "step": step_id,
            "tool": "create_file",
            "description": "Save results to a file",
            "params": {
                "filename": "task_output.txt",
                "content": f"Task: {task}\nCompleted: {datetime.datetime.now().isoformat()}\n\nResults will appear here after execution.",
            },
            "risk": "low",
        })
        step_id += 1

    if any(w in task_lower for w in ["list", "files", "outputs", "directory"]):
        plan.append({
            "step": step_id,
            "tool": "list_files",
            "description": "List all output files",
            "params": {},
            "risk": "low",
        })
        step_id += 1

    # Fallback: general web search
    if not plan:
        plan.append({
            "step": 1,
            "tool": "web_search",
            "description": f"Research task: {task}",
            "params": {"query": task},
            "risk": "low",
        })
        plan.append({
            "step": 2,
            "tool": "summarize_text",
            "description": "Summarize and organize findings",
            "params": {"text": f"Research findings about: {task}"},
            "risk": "low",
        })
        plan.append({
            "step": 3,
            "tool": "create_file",
            "description": "Save final report to file",
            "params": {
                "filename": "research_report.txt",
                "content": f"Research Report\n{'='*40}\nTask: {task}\nDate: {datetime.datetime.now().isoformat()}\n",
            },
            "risk": "low",
        })

    return plan


# ──────────────────────────────────────────
# AGENT STATE MANAGER
# ──────────────────────────────────────────

class TaskAgent:
    """Manages the full lifecycle of a task: plan → approve → execute."""

    def __init__(self):
        self.sessions: dict[str, dict] = {}

    def create_session(self, session_id: str, task: str) -> dict:
        plan = generate_plan(task)
        session = {
            "session_id": session_id,
            "task": task,
            "status": "pending_approval",
            "plan": plan,
            "results": [],
            "created_at": datetime.datetime.now().isoformat(),
            "approved_steps": [],
            "rejected_steps": [],
        }
        self.sessions[session_id] = session
        return session

    def approve_plan(self, session_id: str, approved_steps: list[int]) -> dict:
        session = self.sessions.get(session_id)
        if not session:
            return {"error": "Session not found"}

        session["approved_steps"] = approved_steps
        session["rejected_steps"] = [
            s["step"] for s in session["plan"] if s["step"] not in approved_steps
        ]
        session["status"] = "executing"
        return session

    def execute_session(self, session_id: str) -> dict:
        session = self.sessions.get(session_id)
        if not session:
            return {"error": "Session not found"}

        results = []
        for step in session["plan"]:
            if step["step"] in session["approved_steps"]:
                result = execute_tool(step["tool"], step["params"])
                result["step"] = step["step"]
                result["description"] = step["description"]
                results.append(result)
            else:
                results.append({
                    "step": step["step"],
                    "tool": step["tool"],
                    "description": step["description"],
                    "status": "skipped",
                    "result": "Step was not approved by user.",
                    "timestamp": datetime.datetime.now().strftime("%H:%M:%S"),
                })

        session["results"] = results
        session["status"] = "completed"
        session["completed_at"] = datetime.datetime.now().isoformat()
        return session

    def get_session(self, session_id: str) -> dict | None:
        return self.sessions.get(session_id)


# Singleton agent instance
agent = TaskAgent()
