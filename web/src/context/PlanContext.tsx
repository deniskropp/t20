import { createContext, useContext, useState } from 'react';
import type { ReactNode } from 'react';
import type { Plan, Team } from '../types';
import * as api from '../api';

interface PlanContextType {
    jobId: string | null;
    currentPlan: Plan | null;
    setPlan: (plan: Plan) => void;
    startNewPlan: (goal: string, files?: any[], model?: string) => Promise<void>;
    updateTeam: (team: Team) => void;
    isLoading: boolean;
    error: string | null;
}

const PlanContext = createContext<PlanContextType | undefined>(undefined);

export function PlanProvider({ children }: { children: ReactNode }) {
    const [jobId, setJobId] = useState<string | null>(null);
    const [currentPlan, setCurrentPlan] = useState<Plan | null>(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const startNewPlan = async (goal: string, files: any[] = [], model: string = 'gemini-2.0-flash-exp') => {
        setIsLoading(true);
        setError(null);
        try {
            const response = await api.startWorkflow({ 
                high_level_goal: goal,
                files,
                model
            });
            setJobId(response.jobId);
            // Ensure team object exists
            const plan = response.plan;
            if (!plan.team) {
                plan.team = { notes: '', prompts: [] };
            }
            setCurrentPlan(plan);
        } catch (err: any) {
            setError(err.message || 'Failed to start plan');
        } finally {
            setIsLoading(false);
        }
    };

    const setPlan = (plan: Plan) => {
        setCurrentPlan(plan);
    };

    const updateTeam = (team: Team) => {
        if (!currentPlan) return;
        setCurrentPlan({ ...currentPlan, team });
    };

    return (
        <PlanContext.Provider value={{
            jobId,
            currentPlan,
            setPlan,
            startNewPlan,
            updateTeam,
            isLoading,
            error
        }}>
            {children}
        </PlanContext.Provider>
    );
}

export function usePlan() {
    const context = useContext(PlanContext);
    if (!context) {
        throw new Error('usePlan must be used within a PlanProvider');
    }
    return context;
}
