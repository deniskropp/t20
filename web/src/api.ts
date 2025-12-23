import axios from 'axios';
import type { StartRequest, StartResponse } from './types';

const api = axios.create({
    baseURL: '/api',
});

export const startWorkflow = async (data: StartRequest): Promise<StartResponse> => {
    const response = await api.post('/start', data);
    return response.data;
};
