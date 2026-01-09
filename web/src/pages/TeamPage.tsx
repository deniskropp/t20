import { usePlan } from '../context/PlanContext';
import { Plus, Trash2, Users } from 'lucide-react';

export function TeamPage() {
    const { currentPlan, setPlan } = usePlan();

    if (!currentPlan) {
        return (
            <div className="p-8 text-center text-muted-foreground">
                No active plan. Please go to the Home page to start a new plan.
            </div>
        );
    }

    const roles = currentPlan.roles || [];

    const handleAddRole = () => {
        const newRoles = [...roles, { title: '', purpose: '' }];
        setPlan({ ...currentPlan, roles: newRoles });
    };

    const handleRemoveRole = (index: number) => {
        const newRoles = [...roles];
        newRoles.splice(index, 1);
        setPlan({ ...currentPlan, roles: newRoles });
    };

    const handleRoleChange = (index: number, field: 'title' | 'purpose', value: string) => {
        const newRoles = [...roles];
        newRoles[index] = { ...newRoles[index], [field]: value };
        setPlan({ ...currentPlan, roles: newRoles });
    };

    return (
        <div className="space-y-6">
             <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-2xl font-bold">Team Setup & Recruitment</h1>
                    <p className="text-muted-foreground">Define the roles required for this plan.</p>
                </div>
                <button
                    onClick={handleAddRole}
                    className="flex items-center gap-2 px-4 py-2 bg-primary text-primary-foreground rounded-md hover:bg-primary/90 transition-colors"
                >
                    <Plus className="w-4 h-4" />
                    Add Role
                </button>
            </div>

            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                {roles.map((role, index) => (
                    <div key={index} className="border rounded-lg p-4 bg-card shadow-sm space-y-4 relative group">
                        <div className="absolute top-4 right-4 text-muted-foreground opacity-50">
                            <Users className="w-5 h-5" />
                        </div>
                        
                        <div className="space-y-2">
                            <label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">Role Title</label>
                            <input
                                type="text"
                                value={role.title}
                                onChange={(e) => handleRoleChange(index, 'title', e.target.value)}
                                className="w-full px-3 py-2 border-b-2 bg-transparent focus:border-primary focus:outline-none font-medium"
                                placeholder="e.g. Researcher"
                            />
                        </div>

                        <div className="space-y-2">
                            <label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">Purpose</label>
                            <textarea
                                value={role.purpose}
                                onChange={(e) => handleRoleChange(index, 'purpose', e.target.value)}
                                className="w-full p-2 border rounded bg-muted/50 text-sm focus:bg-background focus:outline-none focus:ring-1 focus:ring-primary"
                                placeholder="What is this role responsible for?"
                                rows={3}
                            />
                        </div>

                        <button
                            onClick={() => handleRemoveRole(index)}
                            className="w-full py-2 flex items-center justify-center gap-2 text-destructive hover:bg-destructive/10 rounded-md transition-colors opacity-0 group-hover:opacity-100"
                        >
                            <Trash2 className="w-4 h-4" />
                            Remove Role
                        </button>
                    </div>
                ))}
                
                {roles.length === 0 && (
                     <div className="col-span-full text-center py-12 text-muted-foreground border-2 border-dashed rounded-lg">
                        No roles defined. Define roles to assign tasks to.
                    </div>
                )}
            </div>
        </div>
    );
}
