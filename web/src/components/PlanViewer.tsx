import type { Plan } from '../types';
import { CheckCircle2, Circle, User, Loader2 } from 'lucide-react';
import { cn } from '../lib/utils';

interface PlanViewerProps {
    plan: Plan;
    taskStatuses: Record<string, 'pending' | 'running' | 'completed' | 'failed'>;
}

export function PlanViewer({ plan, taskStatuses }: PlanViewerProps) {
    return (
        <div className="bg-card rounded-lg border shadow-sm h-full flex flex-col">
            <div className="p-4 border-b bg-muted/30">
                <h3 className="font-semibold text-sm uppercase tracking-wider text-muted-foreground">Execution Plan</h3>
                <div className="mt-2 text-lg font-medium leading-snug">{plan.high_level_goal}</div>
            </div>
            <div className="p-4 space-y-3 flex-1 overflow-y-auto">
                {plan.tasks.map((task) => {
                    const status = taskStatuses[task.id] || 'pending';

                    return (
                        <div key={task.id} className={cn(
                            "flex gap-3 p-3 rounded-lg border transition-all duration-300",
                            status === 'running' ? "bg-accent border-primary ring-1 ring-primary/20" : "bg-card",
                            status === 'completed' ? "bg-muted/20 border-border" : "",
                            status === 'pending' ? "opacity-70" : ""
                        )}>
                            <div className="mt-1 shrink-0">
                                {status === 'completed' && <CheckCircle2 className="w-5 h-5 text-green-600" />}
                                {status === 'running' && <Loader2 className="w-5 h-5 text-primary animate-spin" />}
                                {status === 'pending' && <Circle className="w-5 h-5 text-muted-foreground" />}
                                {status === 'failed' && <Circle className="w-5 h-5 text-destructive" />}
                            </div>
                            <div className="min-w-0">
                                <div className="font-medium text-sm text-foreground/90">
                                    {task.description}
                                </div>
                                <div className="flex items-center gap-2 mt-2 text-xs text-muted-foreground">
                                    <span className="flex items-center gap-1 bg-muted px-1.5 py-0.5 rounded text-foreground/70">
                                        <User className="w-3 h-3" /> {task.agent}
                                    </span>
                                    <span className="opacity-50">•</span>
                                    <span className="uppercase text-[10px] tracking-wide">{task.role}</span>
                                </div>
                            </div>
                        </div>
                    )
                })}
            </div>
        </div>
    )
}
