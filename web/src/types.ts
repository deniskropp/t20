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
    requires: string[];
}

export interface Plan {
    high_level_goal: string;
    reasoning: string;
    roles: Role[];
    tasks: Task[];
    team: Team;
}

export interface StartRequest {
    high_level_goal: string;
    files?: File[];
    plan_from?: string;
    orchestrator?: string;
    model?: string;
}

export interface StartResponse {
    jobId: string;
    plan: Plan;
    statusStreamUrl: string;
}

export interface Artifact {
    files?: File[];
}

export interface AgentOutput {
    output: string;
    artifact?: Artifact;
    team?: Team;
}

export interface TaskResult {
    step: Task;
    result: string; // The raw string result (could be JSON of AgentOutput)
}

export interface RunSummary {
    jobId: string;
    highLevelGoal: string;
    startTime: string;
    endTime?: string;
    status: string;
}

export interface ErrorResponse {
    code: string;
    message: string;
    details?: Record<string, any>;
}

export interface RunStateDetail {
    jobId: string;
    plan: Plan;
    executionLog: { step: Task; result: AgentOutput }[];
    finalStatus: string;
    error?: ErrorResponse;
}
