import type { Prompt } from '../types';
import { Plus, Trash2 } from 'lucide-react';

interface PromptEditorProps {
    prompts: Prompt[];
    onChange: (prompts: Prompt[]) => void;
}

export function PromptEditor({ prompts, onChange }: PromptEditorProps) {
    const handleAdd = () => {
        onChange([...prompts, { agent: '', role: '', system_prompt: '' }]);
    };

    const handleRemove = (index: number) => {
        const newPrompts = [...prompts];
        newPrompts.splice(index, 1);
        onChange(newPrompts);
    };

    const handleChange = (index: number, field: keyof Prompt, value: string) => {
        const newPrompts = [...prompts];
        newPrompts[index] = { ...newPrompts[index], [field]: value };
        onChange(newPrompts);
    };

    return (
        <div className="space-y-4">
            <div className="flex items-center justify-between">
                <h3 className="text-lg font-semibold">Prompt Designer</h3>
                <button
                    onClick={handleAdd}
                    className="flex items-center gap-2 px-3 py-1.5 bg-primary text-primary-foreground rounded-md text-sm hover:bg-primary/90 transition-colors"
                >
                    <Plus className="w-4 h-4" />
                    Add Prompt
                </button>
            </div>
            
            <div className="grid gap-4">
                {prompts.map((prompt, index) => (
                    <div key={index} className="border rounded-lg p-4 bg-card space-y-3 relative group">
                        <button
                            onClick={() => handleRemove(index)}
                            className="absolute top-2 right-2 p-1 text-muted-foreground hover:text-destructive opacity-0 group-hover:opacity-100 transition-opacity"
                        >
                            <Trash2 className="w-4 h-4" />
                        </button>
                        
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div className="space-y-2">
                                <label className="text-sm font-medium">Agent Name</label>
                                <input
                                    type="text"
                                    value={prompt.agent}
                                    onChange={(e) => handleChange(index, 'agent', e.target.value)}
                                    className="w-full px-3 py-2 border rounded-md bg-background focus:outline-none focus:ring-2 focus:ring-primary/50"
                                    placeholder="e.g. Researcher"
                                />
                            </div>
                            <div className="space-y-2">
                                <label className="text-sm font-medium">Role</label>
                                <input
                                    type="text"
                                    value={prompt.role}
                                    onChange={(e) => handleChange(index, 'role', e.target.value)}
                                    className="w-full px-3 py-2 border rounded-md bg-background focus:outline-none focus:ring-2 focus:ring-primary/50"
                                    placeholder="e.g. Research Analyst"
                                />
                            </div>
                        </div>
                        
                        <div className="space-y-2">
                            <label className="text-sm font-medium">System Prompt</label>
                            <textarea
                                value={prompt.system_prompt}
                                onChange={(e) => handleChange(index, 'system_prompt', e.target.value)}
                                className="w-full px-3 py-2 border rounded-md bg-background min-h-[100px] font-mono text-sm focus:outline-none focus:ring-2 focus:ring-primary/50"
                                placeholder="You are a helpful assistant..."
                            />
                        </div>
                    </div>
                ))}
                
                {prompts.length === 0 && (
                    <div className="text-center py-8 text-muted-foreground border-2 border-dashed rounded-lg">
                        No prompts defined. Click "Add Prompt" to start.
                    </div>
                )}
            </div>
        </div>
    );
}
