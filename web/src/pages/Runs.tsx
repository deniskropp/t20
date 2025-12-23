import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { listRuns } from '../api';
import type { RunSummary } from '../types';
import { Loader2, Play, CheckCircle2, Clock, XCircle, AlertCircle } from 'lucide-react';


const getStatusIcon = (status: string) => {
    switch (status.toLowerCase()) {
        case 'completed':
        case 'success':
            return <CheckCircle2 className="w-4 h-4 text-green-500" />;
        case 'running':
        case 'in_progress':
            return <Loader2 className="w-4 h-4 text-blue-500 animate-spin" />;
        case 'failed':
        case 'error':
            return <XCircle className="w-4 h-4 text-red-500" />;
        default:
            return <AlertCircle className="w-4 h-4 text-zinc-500" />;
    }
};

const formatDate = (dateStr: string) => {
    try {
        return new Date(dateStr).toLocaleString();
    } catch {
        return dateStr;
    }
};

export function Runs() {
    const [runs, setRuns] = useState<RunSummary[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        loadRuns();
    }, []);

    const loadRuns = async () => {
        try {
            const data = await listRuns();
            // Sort by startTime descending (newest first)
            const sorted = data.sort((a, b) =>
                new Date(b.startTime).getTime() - new Date(a.startTime).getTime()
            );
            setRuns(sorted);
        } catch (e) {
            console.error("Failed to list runs", e);
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return (
            <div className="flex justify-center p-12">
                <Loader2 className="w-8 h-8 animate-spin text-primary" />
            </div>
        );
    }

    return (
        <div className="space-y-6 max-w-6xl mx-auto">
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-2xl font-bold tracking-tight">Execution History</h1>
                    <p className="text-muted-foreground text-sm mt-1">
                        View and manage previous workflow runs
                    </p>
                </div>
            </div>

            {runs.length === 0 ? (
                <div className="bg-card border rounded-xl p-12 text-center text-muted-foreground">
                    <div className="flex justify-center mb-4">
                        <Play className="w-12 h-12 opacity-20" />
                    </div>
                    <h3 className="text-lg font-medium mb-2">No runs yet</h3>
                    <p className="mb-6">Start your first workflow to see it here.</p>
                    <Link to="/" className="inline-flex items-center gap-2 px-4 py-2 bg-primary text-primary-foreground rounded-md hover:bg-primary/90">
                        <Play className="w-4 h-4" /> Start Workflow
                    </Link>
                </div>
            ) : (
                <div className="bg-card border rounded-xl overflow-hidden shadow-sm">
                    <div className="overflow-x-auto">
                        <table className="w-full text-sm text-left">
                            <thead className="bg-muted/50 text-muted-foreground uppercase text-xs font-medium">
                                <tr>
                                    <th className="px-6 py-3 w-32">Status</th>
                                    <th className="px-6 py-3">Goal</th>
                                    <th className="px-6 py-3 w-48">Started</th>
                                    <th className="px-6 py-3 w-32">Duration</th>
                                    <th className="px-6 py-3 w-24">Actions</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-border">
                                {runs.map((run) => (
                                    <tr key={run.jobId} className="hover:bg-muted/30 transition-colors">
                                        <td className="px-6 py-4">
                                            <div className="flex items-center gap-2">
                                                {getStatusIcon(run.status)}
                                                <span className="capitalize">{run.status}</span>
                                            </div>
                                        </td>
                                        <td className="px-6 py-4 font-medium">
                                            <Link to={`/run/${run.jobId}`} className="hover:underline hover:text-primary block truncate max-w-md" title={run.highLevelGoal}>
                                                {run.highLevelGoal}
                                            </Link>
                                            <div className="text-xs text-muted-foreground font-mono mt-1 opacity-70">
                                                ID: {run.jobId.substring(0, 8)}
                                            </div>
                                        </td>
                                        <td className="px-6 py-4 text-muted-foreground whitespace-nowrap">
                                            <div className="flex items-center gap-2">
                                                <Clock className="w-3.5 h-3.5" />
                                                {formatDate(run.startTime)}
                                            </div>
                                        </td>
                                        <td className="px-6 py-4 text-muted-foreground font-mono text-xs">
                                            {run.endTime ? (
                                                ((new Date(run.endTime).getTime() - new Date(run.startTime).getTime()) / 1000).toFixed(1) + 's'
                                            ) : (
                                                '-'
                                            )}
                                        </td>
                                        <td className="px-6 py-4">
                                            <Link
                                                to={`/run/${run.jobId}`}
                                                className="text-primary hover:text-primary/80 font-medium text-xs border border-primary/20 px-3 py-1.5 rounded hover:bg-primary/5 transition-colors"
                                            >
                                                View
                                            </Link>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>
            )}
        </div>
    );
}
