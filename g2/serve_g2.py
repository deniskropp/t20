"""
This module implements the G2 version of the Multi-Agent Workflow API,
as defined in openapi_g2.yaml. It uses FastAPI to create a web server
that provides endpoints for orchestrating multi-agent workflows.
"""

import asyncio
import datetime
import json
import os
import uuid
from typing import List, Optional, Dict, Any, Literal
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, HttpUrl
from sse_starlette.sse import EventSourceResponse

# --- Runtime Imports ---
from runtime.system import System
from runtime.util import read_file as runtime_read_file
from runtime.custom_types import File as RuntimeFile
from runtime import Plan as RuntimePlan

# --- Pydantic Models from openapi_g2.yaml ---

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
    deps: List[str]

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
    high_level_goal: str
    files: Optional[List[File]] = []
    plan_from: Optional[str] = None
    orchestrator: str = "Meta-AI"
    model: str = "gemini-2.5-flash-lite"

class StartResponseG2(BaseModel):
    jobId: str
    plan: Plan
    statusStreamUrl: HttpUrl

class RunRequest(BaseModel):
    plan: RuntimePlan
    rounds: int = 1
    files: Optional[List[File]] = []

class RunInitiatedResponseG2(BaseModel):
    jobId: str
    status: str
    statusStreamUrl: HttpUrl
    controlUrl: HttpUrl

class ErrorResponse(BaseModel):
    code: str
    message: str
    details: Optional[Dict[str, Any]] = None

class StepResultSummary(BaseModel):
    stepId: str
    agent: str
    status: Literal["completed", "failed", "skipped"]
    output: str

class RunStatusResponseG2(BaseModel):
    jobId: str
    status: Literal["pending", "running", "completed", "failed", "paused", "cancelling", "cancelled"]
    results: Optional[List[StepResultSummary]] = None
    error: Optional[ErrorResponse] = None

# --- Workflow Event Schemas ---

class StepStartedEventDetails(BaseModel):
    stepId: str
    agent: str

class StepStartedEvent(BaseModel):
    type: Literal["StepStarted"] = "StepStarted"
    timestamp: datetime.datetime = Field(default_factory=datetime.datetime.now)
    details: StepStartedEventDetails

class AgentOutputReceivedEventDetails(BaseModel):
    stepId: str
    agent: str
    outputSummary: str

class AgentOutputReceivedEvent(BaseModel):
    type: Literal["AgentOutputReceived"] = "AgentOutputReceived"
    timestamp: datetime.datetime = Field(default_factory=datetime.datetime.now)
    details: AgentOutputReceivedEventDetails

class StepCompletedEventDetails(BaseModel):
    stepId: str
    agent: str
    result: Dict[str, Any]

class StepCompletedEvent(BaseModel):
    type: Literal["StepCompleted"] = "StepCompleted"
    timestamp: datetime.datetime = Field(default_factory=datetime.datetime.now)
    details: StepCompletedEventDetails

class WorkflowCompletedEvent(BaseModel):
    type: Literal["WorkflowCompleted"] = "WorkflowCompleted"
    timestamp: datetime.datetime = Field(default_factory=datetime.datetime.now)
    details: Dict[str, Any]

class WorkflowFailedEvent(BaseModel):
    type: Literal["WorkflowFailed"] = "WorkflowFailed"
    timestamp: datetime.datetime = Field(default_factory=datetime.datetime.now)
    details: Dict[str, Any]

class WorkflowPausedEvent(BaseModel):
    type: Literal["WorkflowPaused"] = "WorkflowPaused"
    timestamp: datetime.datetime = Field(default_factory=datetime.datetime.now)
    details: Dict[str, Any]

class WorkflowResumedEvent(BaseModel):
    type: Literal["WorkflowResumed"] = "WorkflowResumed"
    timestamp: datetime.datetime = Field(default_factory=datetime.datetime.now)
    details: Dict[str, Any]

WorkflowEvent = (
    StepStartedEvent | AgentOutputReceivedEvent | StepCompletedEvent |
    WorkflowCompletedEvent | WorkflowFailedEvent | WorkflowPausedEvent | WorkflowResumedEvent
)


class ControlCommand(BaseModel):
    command: Literal["pause", "resume", "cancel"]

class WebhookSubscription(BaseModel):
    webhookId: Optional[str] = None
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
    executionLog: List[Dict[str, Any]] # Placeholder for AgentOutput
    finalStatus: str
    error: Optional[ErrorResponse] = None

class Artifact(BaseModel):
    task: str
    files: List[File]

class AgentOutput(BaseModel):
    output: str
    artifact: Optional[Artifact] = None
    team: Optional[Team] = None
    reasoning: Optional[str] = None

# --- FastAPI Application ---

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initializes the system on server startup."""
    system.setup(orchestrator_name="Meta-AI")
    print("System initialized.")
    yield
    print("System shutdown.")

app = FastAPI(
    title="Multi-Agent Workflow API (G2)",
    version="2.0.0",
    description="API for orchestrating multi-agent workflows with real-time streaming, control, and webhook support.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for jobs, plans, and webhooks
JOBS: Dict[str, Dict[str, Any]] = {}
WEBHOOKS: Dict[str, WebhookSubscription] = {}
BASE_URL = "http://localhost:8000"
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# --- System Initialization ---
# Global system instance
system = System(root_dir=PROJECT_ROOT, default_model="gemini-2.5-flash")


# --- API Endpoints ---

@app.post("/start", response_model=StartResponseG2, status_code=status.HTTP_202_ACCEPTED)
async def start_workflow_g2(request: StartRequest):
    """Initialize the system and create a workflow plan."""
    job_id = str(uuid.uuid4())
    
    runtime_files = [RuntimeFile(path=f.path, content=f.content) for f in request.files]
    
    try:
        plan_from_file = None
        if request.plan_from:
            plan_content = runtime_read_file(request.plan_from)
            plan_from_file = RuntimePlan.model_validate_json(plan_content)

        plan = await system.start(
            high_level_goal=request.high_level_goal,
            files=runtime_files,
            plan=plan_from_file
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate plan: {e}")

    JOBS[job_id] = {"plan": plan, "status": "pending", "request": request, "results": [], "events": asyncio.Queue()}
    
    # Convert RuntimePlan to API Plan model
    api_plan = Plan.model_validate(plan.model_dump())

    return StartResponseG2(
        jobId=job_id,
        plan=api_plan,
        statusStreamUrl=f"{BASE_URL}/runs/{job_id}/stream"
    )

@app.post("/runs/{jobId}", response_model=RunInitiatedResponseG2, status_code=status.HTTP_202_ACCEPTED)
async def initiate_run_g2(request: RunRequest, jobId: str):
    """Initiate the execution of a workflow plan."""
    if jobId not in JOBS:
        raise HTTPException(status_code=404, detail="Job ID not found.")
    job_id = jobId
    # Store the run request for later use, especially for streaming
    JOBS[job_id]["run_request"] = request
    JOBS[job_id]["startTime"] = datetime.datetime.now()

    return RunInitiatedResponseG2(
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
        async for step, result in system.run(plan=runtime_plan, rounds=request.rounds, files=runtime_files):
            result = AgentOutput.model_validate_json(result).model_dump()

            await event_queue.put(StepStartedEvent(details=StepStartedEventDetails(stepId=step.id, agent=step.agent)))
            await event_queue.put(AgentOutputReceivedEvent(details=AgentOutputReceivedEventDetails(stepId=step.id, agent=step.agent, outputSummary=str(result)[:200])))
            await event_queue.put(StepCompletedEvent(details=StepCompletedEventDetails(stepId=step.id, agent=step.agent, result=result)))
            
            job["results"].append({"step": step.model_dump(), "result": result})

        job["status"] = "completed"
        await event_queue.put(WorkflowCompletedEvent(details={"finalStatus": "completed", "overallResultSummary": "Workflow finished successfully."}))

    except Exception as e:
        job["status"] = "failed"
        error_payload = {"code": "execution_failed", "message": str(e)}
        job["error"] = error_payload
        await event_queue.put(WorkflowFailedEvent(details={"finalStatus": "failed", "error": error_payload}))
        print(f"Job {job_id} failed: {e}")


@app.get("/runs/{jobId}", response_model=RunStatusResponseG2)
async def get_run_status_g2(jobId: str):
    """Retrieve the current status and summary results of a workflow execution."""
    job = JOBS.get(jobId)
    if not job:
        raise HTTPException(status_code=404, detail="Job ID not found.")
    
    results = [
        StepResultSummary(
            stepId=res["step"]["id"],
            agent=res["step"]["agent"],
            status="completed", # Simplified for now
            output=str(res["result"])[:200] # Truncate output
        ) for res in job.get("results", [])
    ]

    return RunStatusResponseG2(
        jobId=jobId, 
        status=job["status"],
        results=results,
        error=ErrorResponse.model_validate(job["error"]) if "error" in job else None
    )

async def event_generator(job_id: str):
    """Real event stream generator based on runtime execution."""
    job = JOBS.get(job_id)
    if not job:
        return

    event_queue = job["events"]

    while True:
        try:
            event = await asyncio.wait_for(event_queue.get(), timeout=1.0)
            yield {
                "event": "message", "id": str(uuid.uuid4()),
                "data": json.dumps(event.model_dump(), default=str)
            }
            if isinstance(event, (WorkflowCompletedEvent, WorkflowFailedEvent)):
                break
        except asyncio.TimeoutError:
            # If the job is no longer running, stop the generator
            if job["status"] not in ["pending", "running"]:
                break
            # Otherwise, continue waiting for events
            pass


@app.get("/runs/{jobId}/stream")
async def stream_workflow_events(jobId: str):
    """Stream real-time events for a workflow execution."""
    job = JOBS[jobId]
    if job["status"] == "pending":
        job["status"] = "running"
        
        # Create a RunRequest from the stored plan and original request
        original_request = job["request"]
        run_request = RunRequest(
            plan=job["plan"],
            rounds=original_request.rounds if isinstance(original_request, RunRequest) else 1,
            files=original_request.files
        )
        
        asyncio.create_task(run_workflow_background(jobId, run_request))

    return EventSourceResponse(event_generator(jobId))

@app.post("/runs/{jobId}/control", status_code=status.HTTP_204_NO_CONTENT)
async def control_workflow(jobId: str, command: ControlCommand):
    """Send control commands to a running workflow."""
    job = JOBS.get(jobId)
    if not job:
        raise HTTPException(status_code=404, detail="Job ID not found.")
    
    # Placeholder logic - runtime does not support this yet
    if command.command == "pause":
        job["status"] = "paused"
    elif command.command == "resume":
        job["status"] = "running"
    elif command.command == "cancel":
        job["status"] = "cancelled"
        
    print(f"Job {jobId} received command: {command.command}. New status: {job['status']}")
    return None

@app.post("/webhooks", response_model=Dict[str, str], status_code=status.HTTP_201_CREATED)
async def register_webhook(subscription: WebhookSubscription):
    """Register a new webhook subscription."""
    webhook_id = str(uuid.uuid4())
    subscription.webhookId = webhook_id
    WEBHOOKS[webhook_id] = subscription
    return {"webhookId": webhook_id}

@app.get("/webhooks", response_model=List[WebhookSubscription])
async def list_webhooks():
    """List registered webhook subscriptions."""
    return list(WEBHOOKS.values())

@app.delete("/webhooks/{webhookId}", status_code=status.HTTP_204_NO_CONTENT)
async def unregister_webhook(webhookId: str):
    """Unregister a webhook subscription."""
    if webhookId not in WEBHOOKS:
        raise HTTPException(status_code=404, detail="Webhook ID not found.")
    del WEBHOOKS[webhookId]
    return None

@app.get("/history/runs", response_model=List[RunSummary])
async def list_history_runs(limit: int = 20, offset: int = 0):
    """List historical workflow runs."""
    summaries = []
    sorted_jobs = sorted(JOBS.items(), key=lambda item: item[1].get("startTime", datetime.datetime.min), reverse=True)

    for job_id, job_data in sorted_jobs:
        summary = RunSummary(
            jobId=job_id,
            highLevelGoal=job_data["request"].high_level_goal,
            startTime=job_data.get("startTime", datetime.datetime.now() - datetime.timedelta(minutes=10)), # Placeholder
            status=job_data["status"]
        )
        summaries.append(summary)
    return summaries[offset:offset+limit]

@app.get("/history/runs/{jobId}/state", response_model=RunStateDetail)
async def get_history_run_state(jobId: str):
    """Retrieve the detailed state of a specific historical workflow run."""
    job = JOBS.get(jobId)
    if not job:
        raise HTTPException(status_code=404, detail="Job ID not found.")
    
    return RunStateDetail(
        jobId=jobId,
        plan=Plan.model_validate(job["plan"].model_dump()),
        executionLog=job.get("results", []),
        finalStatus=job["status"],
        error=ErrorResponse.model_validate(job["error"]) if "error" in job else None
    )

if __name__ == "__main__":
    print("Starting G2 API server on http://localhost:8000")
    uvicorn.run("serve_g2:app", host="127.0.0.1", port=8000, reload=False)