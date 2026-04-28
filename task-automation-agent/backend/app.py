"""
Task Automation Agent - FastAPI Server
=======================================
REST API endpoints for the agent UI.
"""

import uuid
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from agent import agent, TOOLS
import os

app = FastAPI(
    title="Task Automation Agent API",
    description="AI agent that plans, seeks approval, and executes tasks.",
    version="1.0.0",
)

# Allow frontend to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve frontend static files
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")


# ──────────────────────────────────────────
# REQUEST / RESPONSE MODELS
# ──────────────────────────────────────────

class TaskRequest(BaseModel):
    task: str

class ApprovalRequest(BaseModel):
    session_id: str
    approved_steps: list[int]


# ──────────────────────────────────────────
# ENDPOINTS
# ──────────────────────────────────────────

@app.get("/")
def root():
    """Serve the frontend."""
    index_path = os.path.join(frontend_path, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Task Automation Agent API is running!", "docs": "/docs"}


@app.get("/health")
def health():
    return {"status": "ok", "agent": "TaskAutomationAgent v1.0"}


@app.get("/tools")
def list_tools():
    """List all available tools the agent can use."""
    return {"tools": TOOLS}


@app.post("/plan")
def create_plan(request: TaskRequest):
    """
    Step 1: Submit a task → get back a proposed execution plan.
    The plan must be approved before execution.
    """
    if not request.task.strip():
        raise HTTPException(status_code=400, detail="Task cannot be empty.")

    session_id = str(uuid.uuid4())
    session = agent.create_session(session_id, request.task)

    return {
        "session_id": session["session_id"],
        "task": session["task"],
        "status": session["status"],
        "plan": session["plan"],
        "message": "Plan generated. Review and approve steps before execution.",
    }


@app.post("/approve")
def approve_plan(request: ApprovalRequest):
    """
    Step 2: Approve specific steps of the plan (human-in-the-loop).
    Send the list of step numbers you want to execute.
    """
    session = agent.get_session(request.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")

    if session["status"] not in ("pending_approval",):
        raise HTTPException(
            status_code=400,
            detail=f"Session is already in status: {session['status']}"
        )

    updated = agent.approve_plan(request.session_id, request.approved_steps)
    return {
        "session_id": updated["session_id"],
        "status": updated["status"],
        "approved_steps": updated["approved_steps"],
        "rejected_steps": updated["rejected_steps"],
        "message": "Approval recorded. Call /execute to run approved steps.",
    }


@app.post("/execute/{session_id}")
def execute_plan(session_id: str):
    """
    Step 3: Execute the approved steps and return results.
    """
    session = agent.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")

    if session["status"] != "executing":
        raise HTTPException(
            status_code=400,
            detail=f"Session must be in 'executing' state. Current: {session['status']}"
        )

    completed = agent.execute_session(session_id)
    return {
        "session_id": completed["session_id"],
        "task": completed["task"],
        "status": completed["status"],
        "results": completed["results"],
        "completed_at": completed.get("completed_at"),
    }


@app.get("/session/{session_id}")
def get_session(session_id: str):
    """Get the full state of a session."""
    session = agent.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")
    return session


@app.get("/sessions")
def list_sessions():
    """List all active sessions (for debugging)."""
    return {
        "sessions": [
            {
                "session_id": k,
                "task": v["task"],
                "status": v["status"],
                "created_at": v["created_at"],
            }
            for k, v in agent.sessions.items()
        ]
    }
