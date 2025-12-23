import { useEffect, useState } from 'react';
import { useLocation, useParams } from 'react-router-dom';
import { getRunState } from '../api';
import type { Plan } from '../types';
import { PlanViewer } from '../components/PlanViewer';
import { ExecutionConsole } from '../components/ExecutionConsole';
import { Layers, Play } from 'lucide-react';

export function Run() {
    const { jobId } = useParams<{ jobId: string }>();
    const location = useLocation();

    const [plan, setPlan] = useState<Plan | null>(location.state?.plan || null);
    const streamUrl = location.state?.streamUrl || `/api/runs/${jobId}/stream`;

    const [events, setEvents] = useState<any[]>([]);
    const [taskStatuses, setTaskStatuses] = useState<Record<string, 'pending' | 'running' | 'completed' | 'failed'>>({});

    const [status, setStatus] = useState<'pending' | 'connecting' | 'running' | 'completed' | 'failed'>('pending');

    useEffect(() => {
        if (!plan && jobId) {
            getRunState(jobId).then(state => {
                setPlan(state.plan);

                // Reconstruct events from log
                const reconstructedEvents = state.executionLog.flatMap(item => [
                    {
                        type: 'StepStarted',
                        details: {
                            stepId: item.step.id,
                            agent: item.step.agent
                        },
                        timestamp: new Date().toISOString()
                    },
                    {
                        type: 'StepCompleted',
                        details: {
                            stepId: item.step.id,
                            result: item.result
                        },
                        timestamp: new Date().toISOString()
                    }
                ]);

                // Add final status event
                if (state.finalStatus === 'completed') {
                    reconstructedEvents.push({
                        type: 'WorkflowCompleted',
                        details: {},
                        timestamp: new Date().toISOString()
                    });
                } else if (state.finalStatus === 'failed') {
                    reconstructedEvents.push({
                        type: 'WorkflowFailed',
                        details: { error: state.error },
                        timestamp: new Date().toISOString()
                    });
                }

                setEvents(reconstructedEvents);

                // Reconstruct statuses
                const newStatuses: Record<string, any> = {};
                state.executionLog.forEach(item => {
                    newStatuses[item.step.id] = 'completed';
                });
                setTaskStatuses(newStatuses);

                setStatus(state.finalStatus as any);
            }).catch(e => console.error("Failed to load run state", e));
        }
    }, [jobId, plan]);

    const startRun = () => {
        // Don't start stream if already finished
        if (status === 'completed' || status === 'failed') return;

        setStatus('connecting');
        const es = new EventSource(streamUrl);

        es.onopen = () => {
            setStatus('running');
        };

        es.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                setEvents(prev => [...prev, data]);

                // Update task status helpers
                if (data.type === 'StepStarted') {
                    const stepId = data.details.stepId;
                    setTaskStatuses(prev => ({ ...prev, [stepId]: 'running' }));
                }
                if (data.type === 'StepCompleted') {
                    const stepId = data.details.stepId;
                    setTaskStatuses(prev => ({ ...prev, [stepId]: 'completed' }));
                }
                if (data.type === 'WorkflowCompleted') {
                    setStatus('completed');
                    es.close();
                }
                if (data.type === 'WorkflowFailed') {
                    setStatus('failed');
                    es.close();
                }

            } catch (e) {
                console.error("Error parsing event", e);
            }
        };

        es.onerror = (e) => {
            console.error("SSE Error", e);
            // Only mark failed if we were actually running, otherwise it might just be connection jitter before start
            if (status === 'running') {
                setStatus('failed');
                es.close();
            }
        };

        return () => es.close();
    };

    useEffect(() => {
        // Auto-start only if we intend to run and haven't loaded a finished state
        if (jobId && status === 'pending') {
            const cleanup = startRun();
            return cleanup;
        }
    }, [jobId, status]);


    if (!plan) return <div className="p-8 text-center">Loading plan...</div>;

    return (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 h-[calc(100vh-8rem)]">
            <div className="lg:col-span-1 flex flex-col gap-4 h-full">
                <h2 className="text-xl font-bold flex items-center gap-2">
                    <Layers className="w-5 h-5" /> Plan
                </h2>
                <div className="flex-1 min-h-0">
                    <PlanViewer plan={plan} taskStatuses={taskStatuses} />
                </div>

                {status === 'completed' && (
                    <div className="p-4 bg-green-500/10 border border-green-500/20 rounded-lg text-green-600 font-medium flex items-center gap-2">
                        <Play className="w-4 h-4 fill-current" /> Workflow Finished
                    </div>
                )}
            </div>
            <div className="lg:col-span-2 flex flex-col gap-4 h-full">
                <h2 className="text-xl font-bold flex items-center gap-2">
                    Execution
                </h2>
                <div className="flex-1 min-h-0">
                    <ExecutionConsole events={events} />
                </div>
            </div>
        </div>
    );
}
