import { useNavigate } from 'react-router-dom';
import { GoalInput } from '../components/GoalInput';
import { usePlan } from '../context/PlanContext';
import { Loader2 } from 'lucide-react';

export function Home() {
    const navigate = useNavigate();
    const { startNewPlan, isLoading } = usePlan();

    const handleStart = async (goal: string, files: any[], model: string) => {
        await startNewPlan(goal, files, model);
        navigate('/design');
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

            {isLoading ? (
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
