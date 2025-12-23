import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { GoalInput } from '../components/GoalInput';
import { startWorkflow } from '../api';
import { Loader2 } from 'lucide-react';

export function Home() {
    const navigate = useNavigate();
    const [loading, setLoading] = useState(false);

    const handleStart = async (goal: string) => {
        setLoading(true);
        try {
            const res = await startWorkflow({ high_level_goal: goal });
            navigate(`/run/${res.jobId}`, { state: { plan: res.plan, streamUrl: res.statusStreamUrl } });
        } catch (e) {
            console.error(e);
            alert("Failed to start workflow. Ensure the backend is running on port 8000.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex flex-col items-center justify-center min-h-[60vh] space-y-8">
            <div className="text-center space-y-4 max-w-2xl">
                <h1 className="text-5xl font-extrabold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-primary to-blue-600 pb-2">
                    What do you want to build?
                </h1>
                <p className="text-muted-foreground text-xl">
                    Describe your objective and let the T20 multi-agent system orchestrate the solution.
                </p>
            </div>

            {loading ? (
                <div className="flex flex-col items-center justify-center py-12 space-y-4">
                    <Loader2 className="w-10 h-10 animate-spin text-primary" />
                    <p className="text-muted-foreground text-lg animate-pulse">Orchestrating plan...</p>
                </div>
            ) : (
                <div className="w-full">
                    <GoalInput onSubmit={handleStart} />
                </div>
            )}
        </div>
    );
}
