import { useEffect, useRef, useState, useMemo } from 'react';
import {
    CheckCircle2,
    AlertCircle,
    Loader2,
    ChevronRight,
    Terminal,
    BrainCircuit,
    FileCode,
    LayoutList
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

// --- Utility for Tailwind classes ---
function cn(...inputs: (string | undefined | null | false)[]) {
    return twMerge(clsx(inputs));
}

// --- Types ---
interface StepData {
    stepId: string;
    agent: string;
    status: 'pending' | 'running' | 'completed' | 'failed';
    output: string;
    reasoning?: string;
    artifacts?: any[]; // Using any for flexibility based on raw JSON
    timestamp: number;
    error?: any;
}

interface WorkflowStatus {
    status: 'idle' | 'running' | 'completed' | 'failed';
    error?: any;
}

// --- Component ---
export function ExecutionConsole({ events }: { events: any[] }) {
    const bottomRef = useRef<HTMLDivElement>(null);
    const containerRef = useRef<HTMLDivElement>(null);

    // Process events into structured steps
    const { steps, workflowStatus } = useMemo(() => {
        const stepsMap = new Map<string, StepData>();
        let wfStatus: WorkflowStatus = { status: 'idle' };

        events.forEach(e => {
            const { type, details, timestamp } = e;

            if (type === 'StepStarted') {
                stepsMap.set(details.stepId, {
                    stepId: details.stepId,
                    agent: details.agent,
                    status: 'running',
                    output: '',
                    timestamp: new Date(timestamp || Date.now()).getTime()
                });
            } else if (type === 'AgentOutputReceived') {
                const step = stepsMap.get(details.stepId);
                if (step) {
                    // This event might be partial or summary, simpler to trust StepCompleted for full data usually,
                    // but we can append if we want streaming feel. 
                    // For now, we trust StepCompleted for the structured result.
                }
            } else if (type === 'StepCompleted') {
                const step = stepsMap.get(details.stepId);
                if (step) {
                    step.status = 'completed';
                    // Parse result
                    const result = details.result || {};
                    step.output = typeof result === 'string' ? result : (result.output || JSON.stringify(result));
                    step.reasoning = result.reasoning;
                    if (result.artifact) {
                        step.artifacts = result.artifact.files || [];
                    }
                }
            } else if (type === 'WorkflowCompleted') {
                wfStatus = { status: 'completed' };
            } else if (type === 'WorkflowFailed') {
                wfStatus = { status: 'failed', error: details.error };
            }
        });

        // Infer running status if we have running steps and haven't finished
        if (wfStatus.status === 'idle' && Array.from(stepsMap.values()).some(s => s.status === 'running')) {
            wfStatus = { status: 'running' };
        }

        return {
            steps: Array.from(stepsMap.values()),
            workflowStatus: wfStatus
        };
    }, [events]);

    // Auto-scroll logic
    useEffect(() => {
        if (workflowStatus.status === 'running' || steps.some(s => s.status === 'running')) {
            bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
        }
    }, [steps.length, workflowStatus.status, events.length]);

    return (
        <div className="bg-[#1e1e1e] rounded-xl border border-[#333] shadow-xl flex flex-col h-full overflow-hidden text-[#d4d4d4] font-sans">
            {/* Header */}
            <div className="p-3 bg-[#252526] border-b border-[#333] flex items-center justify-between shrink-0 z-10">
                <div className="flex items-center gap-2">
                    <div className="p-1.5 bg-primary/10 rounded-md">
                        <Terminal className="w-4 h-4 text-primary" />
                    </div>
                    <span className="font-semibold text-sm tracking-wide">Live Execution</span>
                </div>
                <div className="flex items-center gap-2 text-xs">
                    <span className={cn(
                        "px-2 py-0.5 rounded-full border",
                        workflowStatus.status === 'running' && "bg-yellow-500/10 border-yellow-500/50 text-yellow-500",
                        workflowStatus.status === 'completed' && "bg-green-500/10 border-green-500/50 text-green-500",
                        workflowStatus.status === 'failed' && "bg-red-500/10 border-red-500/50 text-red-500",
                        workflowStatus.status === 'idle' && "bg-gray-500/10 border-gray-500/50 text-gray-500",
                    )}>
                        {workflowStatus.status.toUpperCase()}
                    </span>
                    <span className="text-muted-foreground">{steps.length} Steps</span>
                </div>
            </div>

            {/* Content */}
            <div ref={containerRef} className="flex-1 overflow-y-auto p-4 space-y-4">
                {steps.length === 0 && workflowStatus.status === 'idle' && (
                    <div className="h-full flex flex-col items-center justify-center text-muted-foreground/40 space-y-3">
                        <LayoutList className="w-12 h-12 opacity-20" />
                        <p>Waiting for workflow to start...</p>
                    </div>
                )}

                <AnimatePresence initial={false}>
                    {steps.map((step) => (
                        <StepCard key={step.stepId} step={step} isLast={step === steps[steps.length - 1]} />
                    ))}
                </AnimatePresence>

                {workflowStatus.status === 'completed' && (
                    <motion.div
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="p-4 rounded-lg bg-green-950/20 border border-green-500/20 flex items-center gap-3"
                    >
                        <CheckCircle2 className="w-6 h-6 text-green-500" />
                        <div>
                            <h3 className="font-semibold text-green-400">Workflow Finalized</h3>
                            <p className="text-sm text-green-500/70">All steps completed successfully.</p>
                        </div>
                    </motion.div>
                )}

                {workflowStatus.status === 'failed' && (
                    <motion.div
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="p-4 rounded-lg bg-red-950/20 border border-red-500/20 flex items-start gap-3"
                    >
                        <AlertCircle className="w-6 h-6 text-red-500 shrink-0" />
                        <div>
                            <h3 className="font-semibold text-red-400">Workflow Failed</h3>
                            <p className="text-sm text-red-500/70 mt-1">
                                {workflowStatus.error?.message || "An unexpected error occurred."}
                            </p>
                        </div>
                    </motion.div>
                )}

                <div ref={bottomRef} className="h-4" />
            </div>
        </div>
    );
}

function StepCard({ step, isLast }: { step: StepData, isLast: boolean }) {
    // Auto-expand if running or if it's the last one (and likely interesting)
    const [expanded, setExpanded] = useState(step.status === 'running' || isLast);

    // Update expanded state if status changes to running
    useEffect(() => {
        if (step.status === 'running') setExpanded(true);
    }, [step.status]);

    const statusColor = {
        pending: "border-gray-500/50",
        running: "border-yellow-500",
        completed: "border-green-500",
        failed: "border-red-500"
    }[step.status];

    const bgStatus = {
        pending: "bg-[#2d2d2d]",
        running: "bg-[#2d2d2d]", // active highlight handled by border
        completed: "bg-[#1e1e1e]",
        failed: "bg-[#2d1e1e]"
    }[step.status];

    return (
        <motion.div
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
            className={cn(
                "rounded-lg border-l-4 overflow-hidden transition-colors border-[#333] shadow-sm",
                statusColor,
                bgStatus
            )}
        >
            <button
                onClick={() => setExpanded(!expanded)}
                className="w-full p-3 flex items-center gap-3 hover:bg-white/5 transition-colors text-left"
            >
                {step.status === 'running' ? (
                    <Loader2 className="w-5 h-5 text-yellow-500 animate-spin shrink-0" />
                ) : step.status === 'completed' ? (
                    <CheckCircle2 className="w-5 h-5 text-green-500 shrink-0" />
                ) : step.status === 'failed' ? (
                    <AlertCircle className="w-5 h-5 text-red-500 shrink-0" />
                ) : (
                    <div className="w-5 h-5 rounded-full border-2 border-gray-600 shrink-0" />
                )}

                <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2">
                        <span className="font-mono text-xs font-bold text-primary/80 uppercase tracking-wider bg-primary/10 px-1.5 py-0.5 rounded">
                            {step.agent}
                        </span>
                        <span className="text-sm font-medium truncate block text-zinc-300">
                            Step {step.stepId}
                        </span>
                    </div>
                </div>

                <div className="flex items-center gap-3 text-muted-foreground">
                    <ChevronRight className={cn("w-4 h-4 transition-transform", expanded && "rotate-90")} />
                </div>
            </button>

            <AnimatePresence>
                {expanded && (
                    <motion.div
                        initial={{ height: 0, opacity: 0 }}
                        animate={{ height: "auto", opacity: 1 }}
                        exit={{ height: 0, opacity: 0 }}
                        className="overflow-hidden"
                    >
                        <div className="p-4 pt-0 space-y-3 border-t border-white/5">

                            {/* Reasoning Section - Only show if present */}
                            {step.reasoning && (
                                <div className="mt-3 bg-blue-950/20 border-l-2 border-blue-500/50 p-3 rounded-r text-sm text-blue-200/80">
                                    <div className="flex items-center gap-2 mb-1 text-blue-400 font-semibold text-xs uppercase tracking-wide">
                                        <BrainCircuit className="w-3.5 h-3.5" /> Reasoning
                                    </div>
                                    <div className="italic leading-relaxed">
                                        {step.reasoning}
                                    </div>
                                </div>
                            )}

                            {/* Artifacts - Only show if present */}
                            {step.artifacts && step.artifacts.length > 0 && (
                                <div className="mt-3 flex gap-2 overflow-x-auto pb-1">
                                    {step.artifacts.map((file: any, i: number) => (
                                        <div key={i} className="flex items-center gap-1.5 bg-[#252526] border border-[#3e3e42] px-2 py-1.5 rounded text-xs text-zinc-300 whitespace-nowrap">
                                            <FileCode className="w-3.5 h-3.5 text-blue-400" />
                                            {file.path || "Generated File"}
                                        </div>
                                    ))}
                                </div>
                            )}

                            {/* Main Output */}
                            <div className="mt-3">
                                <div className="text-xs font-mono text-zinc-500 mb-1.5 uppercase tracking-wider">Output</div>
                                <div className="bg-[#000000] p-3 rounded-md border border-[#333] font-mono text-sm leading-relaxed whitespace-pre-wrap text-[#9cdcfe] shadow-inner max-h-[300px] overflow-y-auto custom-scrollbar">
                                    {step.output || <span className="text-zinc-600 italic">No output yet...</span>}
                                </div>
                            </div>
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>
        </motion.div>
    );
}

// Add global style for scrollbar if not exists
const style = document.createElement('style');
style.innerHTML = `
.custom-scrollbar::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}
.custom-scrollbar::-webkit-scrollbar-track {
    background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
    background: #424242;
    border-radius: 3px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
    background: #555;
}
`;
document.head.appendChild(style);

