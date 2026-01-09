import datetime
from typing import List, Optional, Dict, Any, Literal
from sqlalchemy import String, Text, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column
from pydantic import BaseModel, Field, HttpUrl, ConfigDict
from t20_api.database import Base

# --- SQLAlchemy Models ---

class Prompt(Base):
    __tablename__ = "prompts"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[Optional[str]] = mapped_column(String, index=True, nullable=True) 
    type: Mapped[str] = mapped_column(String, index=True) # system, session, team, task
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    metadata_json: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)

# --- Pydantic Models for Prompts ---

class PromptBase(BaseModel):
    name: Optional[str] = None
    type: Literal["system", "session", "team", "task"]
    content: str
    metadata_json: Optional[Dict[str, Any]] = None

class PromptCreate(PromptBase):
    pass

class PromptUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[Literal["system", "session", "team", "task"]] = None
    content: Optional[str] = None
    metadata_json: Optional[Dict[str, Any]] = None

class PromptResponse(PromptBase):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)

# --- Pydantic Models for Workflow (Migrated from main.py) ---

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

class PromptModel(BaseModel):
    agent: str
    role: str
    system_prompt: str

class Team(BaseModel):
    notes: str
    prompts: List[PromptModel]

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
    plan: Plan
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

# Union type for events
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
    executionLog: List[Dict[str, Any]]
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
