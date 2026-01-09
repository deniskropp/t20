import asyncio
import datetime
import json
import os
import uuid
from typing import List, Optional, Dict, Any, Literal

from fastapi import APIRouter, HTTPException, status, BackgroundTasks, Request
from sse_starlette.sse import EventSourceResponse

# --- Runtime Imports ---
from t20.core.system.system import System
from t20.core.common.types import File as RuntimeFile
from t20.core.common.types import Plan as RuntimePlan
from t20.core.common.types import Task as RuntimeTask

from t20_api import models

router = APIRouter(tags=["workflow"])

# In-memory storage
JOBS: Dict[str, Dict[str, Any]] = {}
WEBHOOKS: Dict[str, models.WebhookSubscription] = {}
BASE_URL = "http://localhost:8000"
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../t20'))

# Global system instance
system = System(root_dir=PROJECT_ROOT, default_model="mistral:mistral-small")

def handle_task_started(task: Any):
    """Callback for task_started events from the system message bus."""
    event = models.StepStartedEvent(details=models.StepStartedEventDetails(stepId=task.id, agent=task.agent))
    
    # Broadcast to all running jobs
    for job in JOBS.values():
        if job["status"] == "running":
            job["events"].put_nowait(event)

async def initialize_system(orchestrator_name="Meta-AI"):
    try:
        system.setup(orchestrator_name=orchestrator_name)
    except Exception as e:
        print(f"Warning: System setup failed on startup: {e}")
    
    # Subscribe to task started events
    system.message_bus.subscribe("task_started", handle_task_started)
    print("System initialized.")

async def shutdown_system():
    print("System shutdown.")

# --- Helper Functions ---

def convert_runtime_plan_to_api(runtime_plan: RuntimePlan) -> models.Plan:
    tasks = []
    for t in runtime_plan.tasks:
        tasks.append(models.Task(
            id=t.id,
            description=t.description,
            role=t.role,
            agent=t.agent,
            deps=t.deps
        ))
    
    roles = [models.Role(**r.model_dump()) for r in runtime_plan.roles]
    team = models.Team(**runtime_plan.team.model_dump()) if runtime_plan.team else None
    
    return models.Plan(
        high_level_goal=runtime_plan.high_level_goal,
        reasoning=runtime_plan.reasoning,
        roles=roles,
        tasks=tasks,
        team=team
    )

def convert_api_plan_to_runtime(api_plan: models.Plan) -> RuntimePlan:
    tasks = []
    for t in api_plan.tasks:
        tasks.append(RuntimeTask(
            id=t.id,
            description=t.description,
            role=t.role,
            agent=t.agent,
            deps=t.deps
        ))
    
    from t20.core.common.types import Role as RuntimeRole, Team as RuntimeTeam, Prompt as RuntimePrompt
    
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
    
    try:
        async for task, result in system.run(plan, rounds=rounds, files=files):
            # Check for cancellation
            if job["status"] == "cancelling":
                job["status"] = "cancelled"
                job["events"].put_nowait(models.WorkflowFailedEvent(details={"finalStatus": "cancelled", "error": models.ErrorResponse(code="CANCELLED", message="Workflow cancelled by user.")}))
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
                 job["events"].put_nowait(models.AgentOutputReceivedEvent(details=models.AgentOutputReceivedEventDetails(stepId=task.id, agent=task.agent, outputSummary=summary)))
                 
                 # Try to parse full result if it's JSON
                 try:
                     parsed_res = json.loads(result)
                     job["events"].put_nowait(models.StepCompletedEvent(details=models.StepCompletedEventDetails(stepId=task.id, agent=task.agent, result=parsed_res)))
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
            job["events"].put_nowait(models.WorkflowCompletedEvent(details={"finalStatus": "completed", "overallResultSummary": "Workflow finished successfully."}))

    except Exception as e:
        job["status"] = "failed"
        job["end_time"] = datetime.datetime.now()
        error_resp = models.ErrorResponse(code="EXECUTION_ERROR", message=str(e))
        job["error"] = error_resp
        job["events"].put_nowait(models.WorkflowFailedEvent(details={"finalStatus": "failed", "error": error_resp}))
        print(f"Error in job {job_id}: {e}")

# --- API Endpoints ---

@router.post("/start", response_model=models.StartResponseG2, status_code=202)
async def start_workflow(request: models.StartRequest):
    try:
        runtime_files = [RuntimeFile(path=f.path, content=f.content) for f in (request.files or [])]
        
        if not system.orchestrator:
             system.setup(orchestrator_name=request.orchestrator)

        plan = await system.start(
            high_level_goal=request.high_level_goal,
            files=runtime_files,
            plan=None
        )
        
        api_plan = convert_runtime_plan_to_api(plan)
        job_id = str(uuid.uuid4())
        
        JOBS[job_id] = {
            "id": job_id,
            "high_level_goal": request.high_level_goal,
            "status": "pending",
            "plan": api_plan, 
            "events": asyncio.Queue(),
            "results": [],
            "created_at": datetime.datetime.now(),
            "execution_log": []
        }
        
        return models.StartResponseG2(
            jobId=job_id,
            plan=api_plan,
            statusStreamUrl=f"{BASE_URL}/runs/{job_id}/stream"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/runs/{jobId}", response_model=models.RunInitiatedResponseG2, status_code=202)
async def initiate_run(jobId: str, request: models.RunRequest, background_tasks: BackgroundTasks):
    if jobId not in JOBS:
        raise HTTPException(status_code=404, detail="Job ID not found")
    
    job = JOBS[jobId]
    if job["status"] != "pending":
         raise HTTPException(status_code=409, detail=f"Job is already {job['status']}")

    plan_to_run = request.plan
    job["plan"] = plan_to_run
    
    runtime_plan = convert_api_plan_to_runtime(plan_to_run)
    runtime_files = [RuntimeFile(path=f.path, content=f.content) for f in (request.files or [])]

    background_tasks.add_task(run_workflow_background, jobId, runtime_plan, request.rounds, runtime_files)
    
    return models.RunInitiatedResponseG2(
        jobId=jobId,
        status="running",
        statusStreamUrl=f"{BASE_URL}/runs/{jobId}/stream",
        controlUrl=f"{BASE_URL}/runs/{jobId}/control"
    )

@router.get("/runs/{jobId}", response_model=models.RunStatusResponseG2)
async def get_run_status(jobId: str):
    if jobId not in JOBS:
        raise HTTPException(status_code=404, detail="Job ID not found")
    
    job = JOBS[jobId]
    results_summary = [models.StepResultSummary(**r) for r in job["results"]]
    
    return models.RunStatusResponseG2(
        jobId=jobId,
        status=job["status"],
        results=results_summary,
        error=job.get("error")
    )

@router.get("/runs/{jobId}/stream", response_class=EventSourceResponse)
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
                event = await asyncio.wait_for(queue.get(), timeout=1.0)
                yield {
                    "event": event.type,
                    "data": event.model_dump_json()
                }
                
                if event.type in ["WorkflowCompleted", "WorkflowFailed", "WorkflowCancelled"]:
                    break
                    
            except asyncio.TimeoutError:
                if job["status"] in ["completed", "failed", "cancelled"] and queue.empty():
                    break
                continue
    
    return EventSourceResponse(event_generator())

@router.post("/runs/{jobId}/control", status_code=204)
async def control_workflow(jobId: str, command: models.ControlCommand):
    if jobId not in JOBS:
        raise HTTPException(status_code=404, detail="Job ID not found")
    
    job = JOBS[jobId]
    cmd = command.command
    
    if cmd == "pause":
        if job["status"] == "running":
            job["status"] = "paused"
            job["events"].put_nowait(models.WorkflowPausedEvent(details={"finalStatus": "paused"}))
        else:
            raise HTTPException(status_code=409, detail="Cannot pause. Job is not running.")
            
    elif cmd == "resume":
        if job["status"] == "paused":
            job["status"] = "running"
            job["events"].put_nowait(models.WorkflowResumedEvent(details={"finalStatus": "running"}))
        else:
             raise HTTPException(status_code=409, detail="Cannot resume. Job is not paused.")

    elif cmd == "cancel":
        if job["status"] in ["running", "paused"]:
            job["status"] = "cancelling"
        else:
             raise HTTPException(status_code=409, detail="Cannot cancel. Job is not active.")

@router.post("/webhooks", status_code=201)
async def register_webhook(subscription: models.WebhookSubscription):
    webhook_id = str(uuid.uuid4())
    sub_data = subscription.model_copy()
    sub_data.webhookId = webhook_id
    WEBHOOKS[webhook_id] = sub_data
    return {"webhookId": webhook_id}

@router.get("/webhooks", response_model=List[models.WebhookSubscription])
async def list_webhooks():
    return list(WEBHOOKS.values())

@router.delete("/webhooks/{webhookId}", status_code=204)
async def unregister_webhook(webhookId: str):
    if webhookId in WEBHOOKS:
        del WEBHOOKS[webhookId]
    else:
        raise HTTPException(status_code=404, detail="Webhook not found")

@router.get("/history/runs", response_model=List[models.RunSummary])
async def list_history_runs(limit: int = 20, offset: int = 0, status: Optional[str] = None):
    filtered_jobs = list(JOBS.values())
    if status:
        filtered_jobs = [j for j in filtered_jobs if j["status"] == status]
    
    filtered_jobs.sort(key=lambda x: x["created_at"], reverse=True)
    
    paged = filtered_jobs[offset : offset + limit]
    
    return [
        models.RunSummary(
            jobId=j["id"],
            highLevelGoal=j["high_level_goal"],
            startTime=j["created_at"],
            endTime=j.get("end_time"),
            status=j["status"]
        ) for j in paged
    ]

@router.get("/history/runs/{jobId}/state", response_model=models.RunStateDetail)
async def get_history_run_state(jobId: str):
    if jobId not in JOBS:
        raise HTTPException(status_code=404, detail="Job ID not found")
    
    job = JOBS[jobId]
    return models.RunStateDetail(
        jobId=job["id"],
        plan=job["plan"],
        executionLog=job["execution_log"],
        finalStatus=job["status"],
        error=job.get("error")
    )
