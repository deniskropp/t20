import { useState, useRef } from 'react';
import { ArrowRight, Paperclip, X, File as FileIcon, Sparkles } from 'lucide-react';
import type { File } from '../types';

export function GoalInput({ onSubmit }: { onSubmit: (goal: string, files: File[], model: string) => void }) {
    const [goal, setGoal] = useState('');
    const [files, setFiles] = useState<File[]>([]);
    const [model, setModel] = useState('gemini-1.5-pro');
    const fileInputRef = useRef<HTMLInputElement>(null);

    const templates = [
        "Create a snake game in Python",
        "Analyze this data file",
        "Refactor the authentication module"
    ];

    const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files) {
            const newFiles: File[] = [];
            for (let i = 0; i < e.target.files.length; i++) {
                const file = e.target.files[i];
                const text = await file.text();
                newFiles.push({ path: file.name, content: text });
            }
            setFiles([...files, ...newFiles]);
        }
    };

    const removeFile = (index: number) => {
        setFiles(files.filter((_, i) => i !== index));
    };

    const handleSubmit = () => {
        if (!goal.trim()) return;
        onSubmit(goal, files, model);
    };

    return (
        <div className="relative group max-w-2xl mx-auto space-y-4">
            <div className="flex gap-2 justify-center">
                {templates.map(t => (
                    <button
                        key={t}
                        onClick={() => setGoal(t)}
                        className="text-xs bg-muted/50 hover:bg-muted px-3 py-1.5 rounded-full transition-colors border border-border/50 flex items-center gap-1"
                    >
                        <Sparkles className="w-3 h-3 text-yellow-500" />
                        {t}
                    </button>
                ))}
            </div>

            <div className="relative">
                <div className="absolute -inset-0.5 bg-gradient-to-r from-primary to-blue-600 rounded-lg blur opacity-25 group-hover:opacity-50 transition duration-1000 group-hover:duration-200"></div>
                <div className="relative bg-card ring-1 ring-border rounded-lg p-2 shadow-xl">
                    <textarea
                        value={goal}
                        onChange={(e) => setGoal(e.target.value)}
                        placeholder="Describe your goal..."
                        className="w-full bg-transparent border-0 focus:ring-0 resize-none min-h-[120px] text-lg p-4 outline-none placeholder:text-muted-foreground/50"
                    />

                    {files.length > 0 && (
                        <div className="px-4 py-2 flex flex-wrap gap-2">
                            {files.map((f, i) => (
                                <div key={i} className="flex items-center gap-1 bg-muted px-2 py-1 rounded text-xs">
                                    <FileIcon className="w-3 h-3" />
                                    <span className="max-w-[100px] truncate">{f.path}</span>
                                    <button onClick={() => removeFile(i)} className="hover:text-destructive"><X className="w-3 h-3" /></button>
                                </div>
                            ))}
                        </div>
                    )}

                    <div className="flex justify-between items-center px-2 pb-2 pt-2 border-t border-border/50">
                        <div className="flex items-center gap-2">
                            <button
                                onClick={() => fileInputRef.current?.click()}
                                className="p-2 text-muted-foreground hover:text-foreground transition-colors rounded-full hover:bg-muted"
                                title="Attach files"
                            >
                                <Paperclip className="w-5 h-5" />
                            </button>
                            <input
                                type="file"
                                multiple
                                className="hidden"
                                ref={fileInputRef}
                                onChange={handleFileChange}
                            />

                            <select
                                value={model}
                                onChange={(e) => setModel(e.target.value)}
                                className="bg-transparent text-sm text-muted-foreground hover:text-foreground outline-none cursor-pointer"
                            >
                                <option value="gemini-1.5-pro">Gemini 1.5 Pro</option>
                                <option value="gpt-4o">GPT-4o</option>
                                <option value="claude-3-5-sonnet">Claude 3.5 Sonnet</option>
                            </select>
                        </div>

                        <button
                            onClick={handleSubmit}
                            disabled={!goal.trim()}
                            className="flex items-center gap-2 bg-primary text-primary-foreground px-4 py-2 rounded-md font-medium disabled:opacity-50 disabled:cursor-not-allowed hover:bg-primary/90 transition-all"
                        >
                            Generate Plan <ArrowRight className="w-4 h-4" />
                        </button>
                    </div>
                </div>
            </div>
        </div>
    )
}
