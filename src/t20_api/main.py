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
from fastapi import FastAPI, HTTPException, status, Path, Body, Query, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, HttpUrl
from sse_starlette.sse import EventSourceResponse

# --- Runtime Imports ---
from t20.core.system import System
from t20.core.util import read_file as runtime_read_file
from t20.core.custom_types import File as RuntimeFile
from t20.core.custom_types import Plan as RuntimePlan
from t20.core.custom_types import Task as RuntimeTask

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
    plan: Plan # Expect API Plan structure
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

# In-memory storage
JOBS: Dict[str, Dict[str, Any]] = {}
WEBHOOKS: Dict[str, WebhookSubscription] = {}
BASE_URL = "http://localhost:8000"
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../t20'))

# Global system instance
system = System(root_dir=PROJECT_ROOT, default_model="mistral:mistral-small")

def handle_task_started(task: Any):
    """Callback for task_started events from the system message bus."""
    event = StepStartedEvent(details=StepStartedEventDetails(stepId=task.id, agent=task.agent))
    
    # Broadcast to all running jobs
    # Note: Ideally we should filter by job ID, but System is currently singleton and doesn't explicitly track job ID in `task_started` bus event.
    # In a real multi-job system, we'd need context propagation.
    # For now, we'll broadcast to all running jobs which might be acceptable if we assume single active job or we attach jobId to task context.
    # Since we don't have jobId in task, we might send to all "running" jobs.
    for job in JOBS.values():
        if job["status"] == "running":
            job["events"].put_nowait(event)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initializes the system on server startup."""
    try:
        system.setup(orchestrator_name="Meta-AI")
    except Exception as e:
        print(f"Warning: System setup failed on startup: {e}")
    
    # Subscribe to task started events
    system.message_bus.subscribe("task_started", handle_task_started)
    
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


# --- Helper Functions ---

def convert_runtime_plan_to_api(runtime_plan: RuntimePlan) -> Plan:
    tasks = []
    for t in runtime_plan.tasks:
        tasks.append(Task(
            id=t.id,
            description=t.description,
            role=t.role,
            agent=t.agent,
            deps=t.deps
        ))
    
    roles = [Role(**r.model_dump()) for r in runtime_plan.roles]
    team = Team(**runtime_plan.team.model_dump()) if runtime_plan.team else None
    
    return Plan(
        high_level_goal=runtime_plan.high_level_goal,
        reasoning=runtime_plan.reasoning,
        roles=roles,
        tasks=tasks,
        team=team
    )

def convert_api_plan_to_runtime(api_plan: Plan) -> RuntimePlan:
    tasks = []
    for t in api_plan.tasks:
        tasks.append(RuntimeTask(
            id=t.id,
            description=t.description,
            role=t.role,
            agent=t.agent,
            deps=t.deps
        ))
    
    # For roles and team we can use model_dump since structure matches mostly
    # But strictly constructing is safer
    from t20.core.custom_types import Role as RuntimeRole, Team as RuntimeTeam, Prompt as RuntimePrompt
    
    roles = [RuntimeRole(title=r.title, purpose=r.purpose) for r in api_plan.roles]
    
    team = None
    if api_plan.team:
        prompts = [RuntimePrompt(agent=p.agent, role=p.role, system_prompt=p.system_prompt) for p in api_plan.team.prompts]
        team = RuntimeTeam(notes=api_plan.team.notes, prompts=prompts)

    return RuntimePlan(
        high_level_goal=api_plan.high_level_goal,
        reasoning=api_plan.reasoning,
        roles=roles,
        tasks=tasks,
        team=team
    )

async def run_workflow_background(job_id: str, plan: RuntimePlan, rounds: int, files: List[RuntimeFile]):
    job = JOBS[job_id]
    job["status"] = "running"
    job["start_time"] = datetime.datetime.now()
    
    # Notify start
    # job["events"].put_nowait(WorkflowResumedEvent(details={"finalStatus": "running"})) 

    try:
        async for task, result in system.run(plan, rounds=rounds, files=files):
            # Check for cancellation
            if job["status"] == "cancelling":
                job["status"] = "cancelled"
                job["events"].put_nowait(WorkflowFailedEvent(details={"finalStatus": "cancelled", "error": ErrorResponse(code="CANCELLED", message="Workflow cancelled by user.")}))
                break
            
            # While paused
            while job["status"] == "paused":
                 await asyncio.sleep(1)
                 if job["status"] == "cancelling":
                     break

            # Handle Step Result
            summary = "Output received"
            if result:
                 summary = result[:100] + "..." if len(result) > 100 else result
                 job["events"].put_nowait(AgentOutputReceivedEvent(details=AgentOutputReceivedEventDetails(stepId=task.id, agent=task.agent, outputSummary=summary)))
                 
                 # Try to parse full result if it's JSON
                 try:
                     parsed_res = json.loads(result)
                     job["events"].put_nowait(StepCompletedEvent(details=StepCompletedEventDetails(stepId=task.id, agent=task.agent, result=parsed_res)))
                 except:
                     pass # Not JSON

            job["results"].append({
                "stepId": task.id,
                "agent": task.agent,
                "status": "completed",
                "output": summary
            })
            
        if job["status"] != "cancelled":
            job["status"] = "completed"
            job["end_time"] = datetime.datetime.now()
            job["events"].put_nowait(WorkflowCompletedEvent(details={"finalStatus": "completed", "overallResultSummary": "Workflow finished successfully."}))

    except Exception as e:
        job["status"] = "failed"
        job["end_time"] = datetime.datetime.now()
        error_resp = ErrorResponse(code="EXECUTION_ERROR", message=str(e))
        job["error"] = error_resp
        job["events"].put_nowait(WorkflowFailedEvent(details={"finalStatus": "failed", "error": error_resp}))
        print(f"Error in job {job_id}: {e}")

# --- API Endpoints ---

@app.post("/start", response_model=StartResponseG2, status_code=202)
async def start_workflow(request: StartRequest):
    try:
        runtime_files = [RuntimeFile(path=f.path, content=f.content) for f in (request.files or [])]
        
        # We need to ensure system is setup if not already (e.g. if main wasn't called or lifespan failed)
        if not system.orchestrator:
             system.setup(orchestrator_name=request.orchestrator)

        plan = await system.start(
            high_level_goal=request.high_level_goal,
            files=runtime_files,
            plan=None # We could support plan_from loading here if needed
        )
        
        api_plan = convert_runtime_plan_to_api(plan)
        job_id = str(uuid.uuid4())
        
        JOBS[job_id] = {
            "id": job_id,
            "high_level_goal": request.high_level_goal,
            "status": "pending",
            "plan": api_plan, # Store API plan
            "events": asyncio.Queue(),
            "results": [],
            "created_at": datetime.datetime.now(),
            "execution_log": []
        }
        
        return StartResponseG2(
            jobId=job_id,
            plan=api_plan,
            statusStreamUrl=f"{BASE_URL}/runs/{job_id}/stream"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/runs/{jobId}", response_model=RunInitiatedResponseG2, status_code=202)
async def initiate_run(jobId: str, request: RunRequest, background_tasks: BackgroundTasks):
    if jobId not in JOBS:
        raise HTTPException(status_code=404, detail="Job ID not found")
    
    job = JOBS[jobId]
    if job["status"] != "pending":
         raise HTTPException(status_code=409, detail=f"Job is already {job['status']}")

    # Update plan if provided in request
    plan_to_run = request.plan
    job["plan"] = plan_to_run # Update stored plan
    
    runtime_plan = convert_api_plan_to_runtime(plan_to_run)
    runtime_files = [RuntimeFile(path=f.path, content=f.content) for f in (request.files or [])]

    # Start background execution
    background_tasks.add_task(run_workflow_background, jobId, runtime_plan, request.rounds, runtime_files)
    
    return RunInitiatedResponseG2(
        jobId=jobId,
        status="running", # Will transition to running in background
        statusStreamUrl=f"{BASE_URL}/runs/{jobId}/stream",
        controlUrl=f"{BASE_URL}/runs/{jobId}/control"
    )

@app.get("/runs/{jobId}", response_model=RunStatusResponseG2)
async def get_run_status(jobId: str):
    if jobId not in JOBS:
        raise HTTPException(status_code=404, detail="Job ID not found")
    
    job = JOBS[jobId]
    results_summary = [StepResultSummary(**r) for r in job["results"]]
    
    return RunStatusResponseG2(
        jobId=jobId,
        status=job["status"],
        results=results_summary,
        error=job.get("error")
    )

@app.get("/runs/{jobId}/stream", response_class=EventSourceResponse)
async def stream_workflow_events(jobId: str, request: Request):
    if jobId not in JOBS:
        raise HTTPException(status_code=404, detail="Job ID not found")
    
    job = JOBS[jobId]
    
    async def event_generator():
        queue = job["events"]
        while True:
            if await request.is_disconnected():
                break
            
            try:
                # Wait for event with timeout to check connection/status
                event = await asyncio.wait_for(queue.get(), timeout=1.0)
                yield {
                    "event": event.type,
                    "data": event.model_dump_json()
                }
                
                if event.type in ["WorkflowCompleted", "WorkflowFailed", "WorkflowCancelled"]:
                    break
                    
            except asyncio.TimeoutError:
                # Keep-alive or check if job finished without event (shouldn't happen if logic is correct)
                if job["status"] in ["completed", "failed", "cancelled"] and queue.empty():
                    break
                continue
    
    return EventSourceResponse(event_generator())

@app.post("/runs/{jobId}/control", status_code=204)
async def control_workflow(jobId: str, command: ControlCommand):
    if jobId not in JOBS:
        raise HTTPException(status_code=404, detail="Job ID not found")
    
    job = JOBS[jobId]
    cmd = command.command
    
    if cmd == "pause":
        if job["status"] == "running":
            job["status"] = "paused"
            job["events"].put_nowait(WorkflowPausedEvent(details={"finalStatus": "paused"}))
        else:
            raise HTTPException(status_code=409, detail="Cannot pause. Job is not running.")
            
    elif cmd == "resume":
        if job["status"] == "paused":
            job["status"] = "running"
            job["events"].put_nowait(WorkflowResumedEvent(details={"finalStatus": "running"}))
        else:
             raise HTTPException(status_code=409, detail="Cannot resume. Job is not paused.")

    elif cmd == "cancel":
        if job["status"] in ["running", "paused"]:
            job["status"] = "cancelling"
        else:
             raise HTTPException(status_code=409, detail="Cannot cancel. Job is not active.")

@app.post("/webhooks", status_code=201)
async def register_webhook(subscription: WebhookSubscription):
    webhook_id = str(uuid.uuid4())
    sub_data = subscription.model_copy()
    sub_data.webhookId = webhook_id
    WEBHOOKS[webhook_id] = sub_data
    return {"webhookId": webhook_id}

@app.get("/webhooks", response_model=List[WebhookSubscription])
async def list_webhooks():
    return list(WEBHOOKS.values())

@app.delete("/webhooks/{webhookId}", status_code=204)
async def unregister_webhook(webhookId: str):
    if webhookId in WEBHOOKS:
        del WEBHOOKS[webhookId]
    else:
        raise HTTPException(status_code=404, detail="Webhook not found")

@app.get("/history/runs", response_model=List[RunSummary])
async def list_history_runs(limit: int = 20, offset: int = 0, status: Optional[str] = None):
    # Filter and sort jobs
    filtered_jobs = list(JOBS.values())
    if status:
        filtered_jobs = [j for j in filtered_jobs if j["status"] == status]
    
    # Sort by created_at desc (default)
    filtered_jobs.sort(key=lambda x: x["created_at"], reverse=True)
    
    paged = filtered_jobs[offset : offset + limit]
    
    return [
        RunSummary(
            jobId=j["id"],
            highLevelGoal=j["high_level_goal"],
            startTime=j["created_at"],
            endTime=j.get("end_time"),
            status=j["status"]
        ) for j in paged
    ]

@app.get("/history/runs/{jobId}/state", response_model=RunStateDetail)
async def get_history_run_state(jobId: str):
    if jobId not in JOBS:
        raise HTTPException(status_code=404, detail="Job ID not found")
    
    job = JOBS[jobId]
    return RunStateDetail(
        jobId=job["id"],
        plan=job["plan"],
        executionLog=job["execution_log"], # This would be populated in real impl
        finalStatus=job["status"],
        error=job.get("error")
    )

def main():
    print("Starting T20 API server on http://localhost:8000")
    uvicorn.run("t20_api.main:app", host="127.0.0.1", port=8000, reload=False)

if __name__ == "__main__":
    main()
