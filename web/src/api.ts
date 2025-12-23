import axios from 'axios';
import type { StartRequest, StartResponse, RunSummary, RunStateDetail } from './types';

const api = axios.create({
    baseURL: '/api',
});

export const startWorkflow = async (data: StartRequest): Promise<StartResponse> => {
    const response = await api.post('/start', data);
    return response.data;
};

export const listArtifacts = async (): Promise<string[]> => {
    const response = await api.get('/artifacts');
    // Assuming backend returns a list of file paths or objects. 
    // Adjust logic based on actual backend response if needed.
    return response.data;
};

export const getArtifactContent = async (path: string): Promise<string> => {
    const response = await api.get(`/artifacts/content`, { params: { path } });
    return response.data; // Assuming raw text or JSON with content
};

export const listRuns = async (): Promise<RunSummary[]> => {
    const response = await api.get('/history/runs');
    return response.data;
};

export const getRunState = async (jobId: string): Promise<RunStateDetail> => {
    const response = await api.get(`/history/runs/${jobId}/state`);
    return response.data;
};
