import { useState } from 'react';
import { ArrowRight, Paperclip } from 'lucide-react';

export function GoalInput({ onSubmit }: { onSubmit: (goal: string) => void }) {
    const [goal, setGoal] = useState('');

    return (
        <div className="relative group max-w-2xl mx-auto">
            <div className="absolute -inset-0.5 bg-gradient-to-r from-primary to-blue-600 rounded-lg blur opacity-25 group-hover:opacity-50 transition duration-1000 group-hover:duration-200"></div>
            <div className="relative bg-card ring-1 ring-border rounded-lg p-2 shadow-xl">
                <textarea
                    value={goal}
                    onChange={(e) => setGoal(e.target.value)}
                    placeholder="Describe your goal..."
                    className="w-full bg-transparent border-0 focus:ring-0 resize-none min-h-[120px] text-lg p-4 outline-none placeholder:text-muted-foreground/50"
                />
                <div className="flex justify-between items-center px-2 pb-2">
                    <button className="p-2 text-muted-foreground hover:text-foreground transition-colors rounded-full hover:bg-muted" title="Attach file (Not implemented)">
                        <Paperclip className="w-5 h-5" />
                    </button>
                    <button
                        onClick={() => goal.trim() && onSubmit(goal)}
                        disabled={!goal.trim()}
                        className="flex items-center gap-2 bg-primary text-primary-foreground px-4 py-2 rounded-md font-medium disabled:opacity-50 disabled:cursor-not-allowed hover:bg-primary/90 transition-all"
                    >
                        Generate Plan <ArrowRight className="w-4 h-4" />
                    </button>
                </div>
            </div>
        </div>
    )
}
