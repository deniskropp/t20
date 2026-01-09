import { usePlan } from '../context/PlanContext';
import { PromptEditor } from '../components/PromptEditor';

export function DesignPage() {
    const { currentPlan, updateTeam } = usePlan();
    
    if (!currentPlan) {
        return (
            <div className="p-8 text-center text-muted-foreground">
                No active plan. Please go to the Home page to start a new plan.
            </div>
        );
    }

    const team = currentPlan.team || { notes: '', prompts: [] };

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-2xl font-bold">Prompt Designer</h1>
                    <p className="text-muted-foreground">Configure agent personas and system prompts.</p>
                </div>
            </div>

            <div className="bg-card rounded-lg p-6 border shadow-sm">
                 <div className="mb-6 space-y-2">
                    <label className="text-sm font-medium">Team Notes / Strategy</label>
                    <textarea 
                        value={team.notes}
                        onChange={(e) => updateTeam({ ...team, notes: e.target.value })}
                        className="w-full px-3 py-2 border rounded-md bg-background focus:outline-none focus:ring-2 focus:ring-primary/50"
                        placeholder="General notes about how this team should operate..."
                        rows={3}
                    />
                 </div>

                 <PromptEditor 
                    prompts={team.prompts} 
                    onChange={(newPrompts) => updateTeam({ ...team, prompts: newPrompts })}
                 />
            </div>
        </div>
    );
}
