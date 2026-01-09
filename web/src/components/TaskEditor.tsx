import type { Task } from '../types';
import { Plus, Trash2, GripVertical } from 'lucide-react';

interface TaskEditorProps {
    tasks: Task[];
    onChange: (tasks: Task[]) => void;
    availableAgents: string[];
}

export function TaskEditor({ tasks, onChange, availableAgents }: TaskEditorProps) {
    const handleAdd = () => {
        const newId = `T-${String(tasks.length + 1).padStart(2, '0')}`;
        onChange([
            ...tasks, 
            { 
                id: newId, 
                description: '', 
                role: '', 
                agent: availableAgents[0] || '', 
                deps: [] 
            }
        ]);
    };

    const handleRemove = (index: number) => {
        const newTasks = [...tasks];
        newTasks.splice(index, 1);
        onChange(newTasks);
    };

    const handleChange = (index: number, field: keyof Task, value: any) => {
        const newTasks = [...tasks];
        newTasks[index] = { ...newTasks[index], [field]: value };
        onChange(newTasks);
    };

    return (
        <div className="space-y-4">
            <div className="flex items-center justify-between">
                <h3 className="text-lg font-semibold">Plan Tasks</h3>
                <button
                    onClick={handleAdd}
                    className="flex items-center gap-2 px-3 py-1.5 bg-primary text-primary-foreground rounded-md text-sm hover:bg-primary/90 transition-colors"
                >
                    <Plus className="w-4 h-4" />
                    Add Task
                </button>
            </div>

            <div className="space-y-4">
                {tasks.map((task, index) => (
                    <div key={index} className="flex gap-4 p-4 border rounded-lg bg-card group">
                        <div className="mt-2 text-muted-foreground cursor-move">
                            <GripVertical className="w-5 h-5" />
                        </div>
                        
                        <div className="flex-1 space-y-4">
                            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                                <div className="space-y-2">
                                    <label className="text-xs font-medium text-muted-foreground">ID</label>
                                    <input
                                        type="text"
                                        value={task.id}
                                        onChange={(e) => handleChange(index, 'id', e.target.value)}
                                        className="w-full px-2 py-1 border rounded bg-background text-sm"
                                    />
                                </div>
                                <div className="space-y-2 md:col-span-2">
                                    <label className="text-xs font-medium text-muted-foreground">Description</label>
                                    <input
                                        type="text"
                                        value={task.description}
                                        onChange={(e) => handleChange(index, 'description', e.target.value)}
                                        className="w-full px-2 py-1 border rounded bg-background text-sm"
                                        placeholder="Task description..."
                                    />
                                </div>
                                <div className="space-y-2">
                                    <label className="text-xs font-medium text-muted-foreground">Agent</label>
                                    <select
                                        value={task.agent}
                                        onChange={(e) => handleChange(index, 'agent', e.target.value)}
                                        className="w-full px-2 py-1 border rounded bg-background text-sm"
                                    >
                                        <option value="">Select Agent</option>
                                        {availableAgents.map(agent => (
                                            <option key={agent} value={agent}>{agent}</option>
                                        ))}
                                    </select>
                                </div>
                            </div>
                            
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                <div className="space-y-2">
                                    <label className="text-xs font-medium text-muted-foreground">Depedencies (comma sep IDs)</label>
                                    <input
                                        type="text"
                                        value={task.deps.join(', ')}
                                        onChange={(e) => handleChange(index, 'deps', e.target.value.split(',').map(s => s.trim()).filter(Boolean))}
                                        className="w-full px-2 py-1 border rounded bg-background text-sm"
                                        placeholder="T-01, T-02"
                                    />
                                </div>
                                <div className="space-y-2">
                                    <label className="text-xs font-medium text-muted-foreground">Role (Manual Override)</label>
                                    <input
                                        type="text"
                                        value={task.role}
                                        onChange={(e) => handleChange(index, 'role', e.target.value)}
                                        className="w-full px-2 py-1 border rounded bg-background text-sm"
                                        placeholder="e.g. Researcher (Optional)"
                                    />
                                </div>
                            </div>
                        </div>

                        <button
                            onClick={() => handleRemove(index)}
                            className="text-muted-foreground hover:text-destructive self-start mt-2"
                        >
                            <Trash2 className="w-5 h-5" />
                        </button>
                    </div>
                ))}
            </div>
        </div>
    );
}
