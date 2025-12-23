import { useEffect, useRef } from 'react';
import { CheckCircle2, AlertCircle, Info, Terminal } from 'lucide-react';


export function ExecutionConsole({ events }: { events: any[] }) {
    const bottomRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [events.length]);

    return (
        <div className="bg-card rounded-lg border shadow-sm min-h-[500px] flex flex-col h-full bg-[#1e1e1e] text-[#d4d4d4]">
            <div className="p-3 border-b border-[#333] bg-[#252526] flex items-center gap-2">
                <Terminal className="w-4 h-4 text-primary" />
                <span className="text-sm font-medium">Execution Log</span>
            </div>
            <div className="flex-1 p-4 space-y-4 overflow-y-auto font-mono text-sm">
                {events.length === 0 && (
                    <div className="text-muted-foreground/50 italic">Waiting for execution to start...</div>
                )}
                {events.map((e, i) => (
                    <EventItem key={i} event={e} />
                ))}
                <div ref={bottomRef} />
            </div>
        </div>
    );
}

function EventItem({ event }: { event: any }) {
    const type = event.type;
    const details = event.details || {};

    if (type === 'StepStarted') {
        return ( // No visual output for start since it's immediate in current backend
            <div className="flex gap-2 text-blue-400 opacity-75">
                <Info className="w-4 h-4 mt-0.5 shrink-0" />
                <div>
                    <div>Step <strong>{details.stepId}</strong> started...</div>
                </div>
            </div>
        )
    }
    if (type === 'StepCompleted') {
        const output = details.result?.output;
        const outputStr = typeof output === 'string' ? output : JSON.stringify(output, null, 2);

        return (
            <div className="flex gap-2 text-green-400">
                <CheckCircle2 className="w-4 h-4 mt-0.5 shrink-0" />
                <div className="min-w-0 flex-1">
                    <div>Step <strong>{details.stepId}</strong> completed</div>
                    <div className="mt-2 bg-[#000000] p-3 rounded border border-[#333] whitespace-pre-wrap overflow-x-auto text-[#9cdcfe]">
                        {outputStr}
                    </div>
                </div>
            </div>
        )
    }
    if (type === 'WorkflowCompleted') {
        return (
            <div className="flex gap-2 text-green-500 font-bold border-t border-[#333] pt-4 mt-4">
                <CheckCircle2 className="w-5 h-5 mt-0.5 shrink-0" />
                <div>Workflow Completed Successfully</div>
            </div>
        )
    }
    if (type === 'WorkflowFailed') {
        return (
            <div className="flex gap-2 text-red-500 font-bold border-t border-[#333] pt-4 mt-4">
                <AlertCircle className="w-5 h-5 mt-0.5 shrink-0" />
                <div>Workflow Failed</div>
                <div className="text-sm font-normal text-red-400 mt-1">{JSON.stringify(details.error)}</div>
            </div>
        )
    }

    return null;
}
