"""
This module implements the G7 version of the Multi-Agent Workflow API,
as defined in openapi_g5.md and openapi_g_7.json. It uses FastAPI to create a web server
that provides endpoints for orchestrating multi-agent workflows, including
adaptive intelligence, federation, and advanced workflow management features.
"""

import asyncio
import datetime
import json
import os
import uuid
from typing import List, Optional, Dict, Any, Literal, Union

import uvicorn
from fastapi import FastAPI, HTTPException, status, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, HttpUrl
from sse_starlette.sse import EventSourceResponse

# --- Runtime Imports ---
from runtime.system import System
from runtime.util import read_file as runtime_read_file
from runtime.custom_types import File as RuntimeFile
from runtime import Plan as RuntimePlan

# --- Pydantic Models from openapi_g5.md and openapi_g_7.json ---

class File(BaseModel):
    path: str
    content: str

class Role(BaseModel):
    title: str
    purpose: str

class Task(BaseModel):
    id: str
    description: str
    role: str
    agent: str
    requires: List[str]

class Prompt(BaseModel):
    agent: str
    role: str
    system_prompt: str

class Team(BaseModel):
    notes: str
    prompts: List[Prompt]

class Plan(BaseModel):
    high_level_goal: str
    reasoning: str
    roles: List[Role]
    tasks: List[Task]
    team: Optional[Team] = None

class StartRequest(BaseModel):
    high_level_goal: Optional[str] = None
    definitionId: Optional[str] = None
    files: Optional[List[File]] = []
    plan_from: Optional[str] = None
    orchestrator: str = "Meta-AI"
    model: str = "gemini-2.5-flash-lite"

class StartResponse(BaseModel):
    jobId: str
    plan: Plan
    statusStreamUrl: HttpUrl

class RunRequest(BaseModel):
    plan: RuntimePlan
    rounds: int = 1
    files: Optional[List[File]] = []

class RunInitiatedResponse(BaseModel):
    jobId: str
    status: str
    statusStreamUrl: HttpUrl
    controlUrl: HttpUrl

class ControlCommand(BaseModel):
    command: Literal["pause", "resume", "cancel"]

class HumanInput(BaseModel):
    input: Dict[str, Any]

class WebhookSubscription(BaseModel):
    webhookId: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))
    url: HttpUrl
    events: List[str] = Field(default_factory=lambda: ["workflow_completed", "workflow_failed"])
    secret: Optional[str] = None

class RunSummary(BaseModel):
    jobId: str
    highLevelGoal: str
    startTime: datetime.datetime
    endTime: Optional[datetime.datetime] = None
    status: str

class RunStateDetail(BaseModel):
    jobId: str
    plan: Plan
    executionLog: List[Dict[str, Any]]
    finalStatus: str
    error: Optional[Dict[str, Any]] = None

# --- G3: Advanced Triggering ---

class TriggerConfig(BaseModel):
    # Example for schedule: {"cron": "0 * * * *"}
    # Example for event: {"source": "github", "event_type": "push"}
    pass

class Trigger(BaseModel):
    triggerId: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: Optional[str] = None
    workflowId: str
    type: Literal["schedule", "event"]
    config: Dict[str, Any]
    enabled: bool = True

# --- G4: Workflow Definition ---

class WorkflowDefinition(BaseModel):
    definitionId: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: Optional[str] = None
    definition: Dict[str, Any] # The actual workflow structure

class WorkflowDefinitionVersion(BaseModel):
    versionId: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))
    description: Optional[str] = None
    definition: Dict[str, Any]

# --- G5: Collaboration ---

class ShareRequest(BaseModel):
    userId: Optional[str] = None
    teamId: Optional[str] = None
    role: Literal["viewer", "editor", "executor"]

class Permission(BaseModel):
    permissionId: str
    role: Literal["viewer", "editor", "executor"]
    userId: Optional[str] = None
    teamId: Optional[str] = None

# --- G6: Plugins ---

class Plugin(BaseModel):
    pluginId: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: Optional[str] = None
    imageUrl: Optional[HttpUrl] = None
    endpoint: HttpUrl
    schema: Dict[str, Any]

class EnabledPlugin(BaseModel):
    pluginId: str
    config: Optional[Dict[str, Any]] = None

# --- G7: Adaptive Intelligence ---

class Feedback(BaseModel):
    workflowId: str
    runId: str
    submittedBy: Optional[str] = None
    metrics: Dict[str, Any]
    annotations: Optional[Dict[str, Any]] = None
    timestamp: datetime.datetime = Field(default_factory=datetime.datetime.now)

class InsightsResponse(BaseModel):
    workflowId: str
    generatedAt: datetime.datetime = Field(default_factory=datetime.datetime.now)
    suggestedDefinitions: List[Dict[str, Any]]
    recommendations: List[str]
    confidence: float

class OrchestratorRegistration(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    endpoint: HttpUrl
    capabilities: List[str]
    auth: Dict[str, Any]
    metadata: Optional[Dict[str, Any]] = None

class DelegationRequest(BaseModel):
    targetOrchestratorId: str
    workflowDefinitionId: str
    context: Optional[Dict[str, Any]] = None
    priority: Literal["low", "normal", "high"] = "normal"

class Capability(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    provider: str
    type: Literal["action", "sensor", "transform", "orchestrator"]
    schema: Dict[str, Any]
    examples: Optional[List[Dict[str, Any]]] = None
    metadata: Optional[Dict[str, Any]] = None

class TelemetryEvent(BaseModel):
    eventId: str
    workflowId: str
    runId: str
    eventType: str
    payload: Dict[str, Any]
    timestamp: datetime.datetime

class Policy(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    scope: Literal["workflow", "organization", "federation"]
    rules: Dict[str, Any]
    enabled: bool = True

class SimulationRequest(BaseModel):
    workflowDefinition: Dict[str, Any]
    hypothesis: str
    simulationParameters: Optional[Dict[str, Any]] = None

class SimulationResult(BaseModel):
    resultId: str
    summary: str
    metrics: Dict[str, Any]
    passed: bool

# --- FastAPI Application ---

app = FastAPI(
    title="Multi-Agent Workflow API (G7)",
    version="7.0.0",
    description="API for orchestrating multi-agent workflows with adaptive intelligence, federation, and advanced workflow management.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- In-memory Storage ---
JOBS: Dict[str, Dict[str, Any]] = {}
WEBHOOKS: Dict[str, WebhookSubscription] = {}
TRIGGERS: Dict[str, Trigger] = {}
DEFINITIONS: Dict[str, WorkflowDefinition] = {}
DEFINITION_VERSIONS: Dict[str, List[WorkflowDefinitionVersion]] = {}
PERMISSIONS: Dict[str, List[Permission]] = {}
PLUGINS: Dict[str, Plugin] = {}
ENABLED_PLUGINS: Dict[str, List[EnabledPlugin]] = {}
FEEDBACK_LOG: List[Feedback] = []
ORCHESTRATORS: Dict[str, OrchestratorRegistration] = {}
CAPABILITIES: Dict[str, Capability] = {}
POLICIES: Dict[str, Policy] = {}

BASE_URL = "http://localhost:8000"
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# --- System Initialization ---
# Global system instance
system = System(root_dir=PROJECT_ROOT)

@app.on_event("startup")
async def startup_event():
    """Initializes the system on server startup."""
    system.setup(orchestrator_name="Meta-AI")
    print("System initialized.")


# --- API Endpoints ---

@app.post("/start", response_model=StartResponse, status_code=status.HTTP_202_ACCEPTED)
async def start_workflow_g2(request: StartRequest):
    """Initialize the system and create a workflow plan."""
    job_id = str(uuid.uuid4())
    
    runtime_files = [RuntimeFile(path=f.path, content=f.content) for f in request.files]
    
    try:
        plan_from_file = None
        if request.plan_from:
            plan_content = runtime_read_file(request.plan_from)
            plan_from_file = RuntimePlan.model_validate_json(plan_content)

        plan = system.start(
            high_level_goal=request.high_level_goal,
            files=runtime_files,
            plan=plan_from_file
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate plan: {e}")

    JOBS[job_id] = {"plan": plan, "status": "pending", "request": request, "results": [], "events": asyncio.Queue()}
    
    # Convert RuntimePlan to API Plan model
    api_plan = Plan.model_validate(plan.model_dump())

    return StartResponse(
        jobId=job_id,
        plan=api_plan,
        statusStreamUrl=f"{BASE_URL}/runs/{job_id}/stream"
    )

@app.post("/runs/{jobId}", response_model=RunInitiatedResponse, status_code=status.HTTP_202_ACCEPTED)
async def initiate_run_g2(request: RunRequest, jobId: str):
    """Initiate the execution of a workflow plan."""
    if jobId not in JOBS:
        raise HTTPException(status_code=404, detail="Job ID not found.")
    job_id = jobId
    # Store the run request for later use, especially for streaming
    JOBS[job_id]["run_request"] = request
    JOBS[job_id]["startTime"] = datetime.datetime.now()

    return RunInitiatedResponse(
        jobId=job_id,
        status="pending",
        statusStreamUrl=f"{BASE_URL}/runs/{job_id}/stream",
        controlUrl=f"{BASE_URL}/runs/{job_id}/control"
    )

async def run_workflow_background(job_id: str, request: RunRequest):
    """Runs the workflow in a background task."""
    job = JOBS[job_id]
    event_queue = job["events"]
    runtime_plan = request.plan
    runtime_files = [RuntimeFile(path=f.path, content=f.content) for f in request.files]

    try:
        # The system.run method is a blocking generator.
        # We need to iterate over it in a way that doesn't block the asyncio event loop.
        # asyncio.to_thread runs the blocking code in a separate thread.
        blocking_generator = system.run(plan=runtime_plan, rounds=request.rounds, files=runtime_files)
        
        while True:
            item = await asyncio.to_thread(lambda: next(blocking_generator, None))
            if item is None:
                break # Generator is exhausted

            step, result = item
            await event_queue.put({"type": "step_completed", "stepId": step.id, "result_summary": str(result)[:100]})
            job["results"].append({"step": step.model_dump(), "result": result})

        job["status"] = "completed"
        await event_queue.put({"type": "workflow_completed"})

    except Exception as e:
        job["status"] = "failed"
        job["error"] = {"message": str(e)}
        await event_queue.put({"type": "workflow_failed", "error": str(e)})
        print(f"Job {job_id} failed: {e}")


async def event_generator(job_id: str):
    """Real event stream generator based on runtime execution."""
    job = JOBS.get(job_id)
    if not job:
        # This part of the generator won't be reached if the job doesn't exist,
        # but it's good practice for robustness.
        return

    event_queue = job["events"]

    while True:
        try:
            # Wait for an event from the queue
            event = await asyncio.wait_for(event_queue.get(), timeout=1.0)
            yield {
                "event": "message", "id": str(uuid.uuid4()),
                "data": json.dumps(event.model_dump(), default=str)
            }
            # Stop if the workflow is finished
            if event.get("type") in ["workflow_completed", "workflow_failed"]:
                break
        except asyncio.TimeoutError:
            # If the job is no longer running, stop the generator
            if job.get("status") not in ["pending", "running"]:
                break
            # Otherwise, send a keep-alive or just continue waiting
            pass

@app.get("/runs/{jobId}/stream")
async def stream_workflow_events(jobId: str):
    """Stream real-time events for a workflow execution."""
    if jobId not in JOBS:
        raise HTTPException(status_code=404, detail="Job ID not found.")

    job = JOBS[jobId]
    if job["status"] == "pending":
        job["status"] = "running"
        # The run is initiated via POST /runs/{jobId}, which stores the request.
        # The stream endpoint will trigger the background task.
        run_request = job.get("run_request")
        if run_request:
            asyncio.create_task(run_workflow_background(jobId, run_request))

    return EventSourceResponse(event_generator(jobId))

@app.get("/history/runs/{jobId}/state", response_model=RunStateDetail)
async def get_history_state(jobId: str):
    job = JOBS.get(jobId)
    if not job:
        raise HTTPException(status_code=404, detail="Job ID not found.")

    # Convert RuntimePlan to API Plan model for the response
    api_plan = Plan.model_validate(job["plan"].model_dump())

    return RunStateDetail(
        jobId=jobId,
        plan=api_plan,
        executionLog=job.get("results", []),
        finalStatus=job.get("status", "unknown"),
        error=job.get("error")
    )

if __name__ == "__main__":
    print("Starting G7 API server on http://localhost:8000")
    uvicorn.run("serve_g7:app", host="127.0.0.1", port=8000, reload=True)