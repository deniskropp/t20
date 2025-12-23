import { useState, useEffect } from 'react';
import { ArtifactBrowser } from '../components/ArtifactBrowser';
import { listRuns } from '../api';
import { Loader2, RefreshCw, History } from 'lucide-react';
import type { RunSummary } from '../types';

export function Artifacts() {
    const [runs, setRuns] = useState<RunSummary[]>([]);
    const [selectedJobId, setSelectedJobId] = useState<string | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const fetchRuns = async () => {
        setLoading(true);
        setError(null);
        try {
            const data = await listRuns();
            setRuns(data);
            if (data.length > 0 && !selectedJobId) {
                // Default to most recent (assuming backend returns sorted or we sort)
                // Backend currently sorts reverse chronological, so index 0 is latest
                setSelectedJobId(data[0].jobId);
            }
        } catch (e) {
            console.error("Failed to list runs", e);
            setError("Failed to load runs. Backend might not be ready or no runs exist.");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchRuns();
    }, []);

    const handleRunChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
        setSelectedJobId(e.target.value);
    };

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-bold tracking-tight">Artifacts</h1>
                    <p className="text-muted-foreground">Browse generated files from your workflow runs.</p>
                </div>
                <div className="flex items-center gap-2">
                    <div className="flex items-center gap-2 bg-card border rounded-md px-3 py-1.5">
                        <History className="w-4 h-4 text-muted-foreground" />
                        <select
                            className="bg-transparent border-none text-sm focus:ring-0 cursor-pointer max-w-[200px]"
                            value={selectedJobId || ''}
                            onChange={handleRunChange}
                            disabled={loading || runs.length === 0}
                        >
                            {runs.length === 0 ? <option>No runs available</option> : null}
                            {runs.map(run => (
                                <option key={run.jobId} value={run.jobId}>
                                    {new Date(run.startTime).toLocaleString()} - {run.highLevelGoal.substring(0, 30)}...
                                </option>
                            ))}
                        </select>
                    </div>

                    <button
                        onClick={fetchRuns}
                        className="p-2 text-muted-foreground hover:text-foreground transition-colors hover:bg-muted rounded-full"
                        title="Refresh"
                    >
                        <RefreshCw className={`w-5 h-5 ${loading ? 'animate-spin' : ''}`} />
                    </button>
                </div>
            </div>

            {error ? (
                <div className="p-4 rounded-lg bg-destructive/10 text-destructive border border-destructive/20">
                    {error}
                </div>
            ) : null}

            {loading && runs.length === 0 ? (
                <div className="flex justify-center py-12">
                    <Loader2 className="w-8 h-8 animate-spin text-muted-foreground" />
                </div>
            ) : (
                selectedJobId ? (
                    <ArtifactBrowser jobId={selectedJobId} />
                ) : (
                    <div className="text-center py-12 text-muted-foreground border-2 border-dashed rounded-lg">
                        No run selected or no runs found.
                    </div>
                )
            )}
        </div>
    );
}
