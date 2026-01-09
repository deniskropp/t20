import axios from 'axios';
import type { 
    StartRequest, 
    StartResponse, 
    RunSummary, 
    RunStateDetail, 
    ControlCommand,
    RunStatusResponse,
    Plan
} from './types';

export const api = axios.create({
    baseURL: '/api', // Adjust if needed to match proxy or backend
});

export const startWorkflow = async (data: StartRequest): Promise<StartResponse> => {
    const response = await api.post('/start', data);
    return response.data;
};

export const listArtifacts = async (): Promise<string[]> => {
    // This endpoint wasn't in the provided openapi.json subset but was in original api.ts
    // Keeping it as is or assuming it exists on backend not shown in snippet
    const response = await api.get('/artifacts'); 
    return response.data;
};

export const getArtifactContent = async (path: string): Promise<string> => {
    const response = await api.get(`/artifacts/content`, { params: { path } });
    return response.data;
};

export const listRuns = async (limit: number = 20, offset: number = 0): Promise<RunSummary[]> => {
    const response = await api.get('/history/runs', { params: { limit, offset } });
    return response.data;
};

export const getRunState = async (jobId: string): Promise<RunStateDetail> => {
    const response = await api.get(`/history/runs/${jobId}/state`);
    return response.data;
};

export const getRunStatus = async (jobId: string): Promise<RunStatusResponse> => {
    const response = await api.get(`/runs/${jobId}`);
    return response.data;
};

export const controlRun = async (jobId: string, command: ControlCommand): Promise<void> => {
    await api.post(`/runs/${jobId}/control`, command);
};

export const initiateRun = async (jobId: string, plan: Plan, rounds: number = 1): Promise<void> => {
    await api.post(`/runs/${jobId}`, { plan, rounds });
};
