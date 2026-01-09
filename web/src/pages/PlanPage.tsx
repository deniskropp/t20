import { useNavigate } from 'react-router-dom';
import { usePlan } from '../context/PlanContext';
import { TaskEditor } from '../components/TaskEditor';
import { Play } from 'lucide-react';
import * as api from '../api';

export function PlanPage() {
    const { currentPlan, setPlan, jobId } = usePlan();
    const navigate = useNavigate();

    if (!currentPlan) {
        return (
            <div className="p-8 text-center text-muted-foreground">
                No active plan. Please go to the Home page to start a new plan.
            </div>
        );
    }

    const tasks = currentPlan.tasks || [];
    const availableAgents = currentPlan.team?.prompts.map(p => p.agent) || [];

    const handleRun = async () => {
        if (!jobId || !currentPlan) return;
        try {
            await api.initiateRun(jobId, currentPlan);
            navigate(`/run/${jobId}`);
        } catch (e) {
            console.error(e);
            alert('Failed to start run');
        }
    };
    
    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-2xl font-bold">Planning</h1>
                    <p className="text-muted-foreground">Refine your plan and tasks before execution.</p>
                </div>
                <button
                    onClick={handleRun}
                    className="flex items-center gap-2 px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 transition-colors font-semibold shadow-sm"
                >
                    <Play className="w-4 h-4" />
                    Execute Plan
                </button>
            </div>

            <div className="bg-card p-6 rounded-lg border shadow-sm space-y-4">
                <div className="space-y-2">
                    <label className="text-sm font-medium">Reasoning / Strategy</label>
                    <textarea
                        value={currentPlan.reasoning}
                        onChange={(e) => setPlan({ ...currentPlan, reasoning: e.target.value })}
                        className="w-full px-3 py-2 border rounded-md bg-background"
                        rows={3}
                    />
                </div>

                <hr className="border-border" />

                <TaskEditor
                    tasks={tasks}
                    onChange={(newTasks) => setPlan({ ...currentPlan, tasks: newTasks })}
                    availableAgents={availableAgents}
                />
            </div>
        </div>
    );
}
