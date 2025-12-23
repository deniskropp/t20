import { useState, useEffect } from 'react';
import { ArtifactBrowser } from '../components/ArtifactBrowser';
import { listArtifacts } from '../api';
import { Loader2, RefreshCw } from 'lucide-react';

export function Artifacts() {
    const [artifacts, setArtifacts] = useState<string[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const fetchArtifacts = async () => {
        setLoading(true);
        setError(null);
        try {
            const data = await listArtifacts();
            setArtifacts(data);
        } catch (e) {
            console.error("Failed to list artifacts", e);
            setError("Failed to load artifacts. Backend might not be ready.");
            // Mock data for demonstration if backend fails
            // setArtifacts(["brain/task.md", "brain/implementation_plan.md", "src/hello.py"]);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchArtifacts();
    }, []);

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-bold tracking-tight">Artifacts</h1>
                    <p className="text-muted-foreground">Browse generated files and documentation from the brain.</p>
                </div>
                <button
                    onClick={fetchArtifacts}
                    className="p-2 text-muted-foreground hover:text-foreground transition-colors hover:bg-muted rounded-full"
                    title="Refresh"
                >
                    <RefreshCw className={`w-5 h-5 ${loading ? 'animate-spin' : ''}`} />
                </button>
            </div>

            {error ? (
                <div className="p-4 rounded-lg bg-destructive/10 text-destructive border border-destructive/20">
                    {error}
                </div>
            ) : null}

            {loading && artifacts.length === 0 ? (
                <div className="flex justify-center py-12">
                    <Loader2 className="w-8 h-8 animate-spin text-muted-foreground" />
                </div>
            ) : (
                <ArtifactBrowser artifacts={artifacts} />
            )}
        </div>
    );
}
