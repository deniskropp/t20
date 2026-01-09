export interface File {
    path: string;
    content: string;
}

export interface Prompt {
    agent: string;
    role: string;
    system_prompt: string;
}

export interface Team {
    notes: string;
    prompts: Prompt[];
}

export interface Role {
    title: string;
    purpose: string;
}

export interface Task {
    id: string;
    description: string;
    role: string;
    agent: string;
    deps: string[]; // Changed from requires to deps to match openapi.json Task-Input/Output
}

export interface Plan {
    high_level_goal: string;
    reasoning: string;
    roles: Role[];
    tasks: Task[];
    team?: Team | null; // Made optional/null to match openapi
}

export interface StartRequest {
    high_level_goal: string;
    files?: File[] | null;
    plan_from?: string | null;
    orchestrator?: string;
    model?: string;
}

export interface StartResponse {
    jobId: string;
    plan: Plan;
    statusStreamUrl: string;
    controlUrl?: string; // Added controlUrl
}

export interface RunInitiatedResponse {
    jobId: string;
    status: string;
    statusStreamUrl: string;
    controlUrl: string;
}

export interface Artifact {
    files?: File[];
}

export interface AgentOutput {
    output: string;
    artifact?: Artifact;
    team?: Team;
}

export interface TaskResult { // This matches StepResultSummary roughly, or internal representation
    stepId: string;
    agent: string;
    status: "completed" | "failed" | "skipped";
    output: string;
}

export interface RunSummary {
    jobId: string;
    highLevelGoal: string;
    startTime: string;
    endTime?: string | null;
    status: string;
}

export interface ErrorResponse {
    code: string;
    message: string;
    details?: any;
}

export interface RunStateDetail {
    jobId: string;
    plan: Plan;
    executionLog: any[]; // The openapi says items: additionalProperties: true
    finalStatus: string;
    error?: ErrorResponse | null;
}

export interface ControlCommand {
    command: "pause" | "resume" | "cancel";
}

export interface RunStatusResponse {
    jobId: string;
    status: "pending" | "running" | "completed" | "failed" | "paused" | "cancelling" | "cancelled";
    results?: TaskResult[] | null;
    error?: ErrorResponse | null;
}
