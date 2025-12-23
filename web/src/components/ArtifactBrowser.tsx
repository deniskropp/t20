import { useState } from 'react';
import { FileText, Download, Folder } from 'lucide-react';
import { getArtifactContent } from '../api';

interface ArtifactBrowserProps {
    artifacts: string[];
}

export function ArtifactBrowser({ artifacts }: ArtifactBrowserProps) {
    const [selectedFile, setSelectedFile] = useState<string | null>(null);
    const [content, setContent] = useState<string>('');
    const [loadingContent, setLoadingContent] = useState(false);

    // Simple file tree structure could be implemented here if artifacts are paths
    // For now, we'll list them as a flat list or simple groups

    const handleFileClick = async (path: string) => {
        if (selectedFile === path) return;
        setSelectedFile(path);
        setLoadingContent(true);
        try {
            const data = await getArtifactContent(path);
            setContent(typeof data === 'string' ? data : JSON.stringify(data, null, 2));
        } catch (e) {
            console.error("Failed to load artifact content", e);
            setContent("Error loading content.");
        } finally {
            setLoadingContent(false);
        }
    };

    const handleDownload = () => {
        if (!selectedFile || !content) return;
        const blob = new Blob([content], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = selectedFile.split('/').pop() || 'artifact';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    };

    return (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 h-[70vh]">
            <div className="md:col-span-1 bg-card border rounded-lg overflow-hidden flex flex-col">
                <div className="p-3 border-b bg-muted/30 font-medium flex items-center gap-2">
                    <Folder className="w-4 h-4 text-blue-500" /> Artifacts
                </div>
                <div className="flex-1 overflow-y-auto p-2 space-y-1">
                    {artifacts.length === 0 ? (
                        <div className="text-muted-foreground text-sm p-4 text-center">No artifacts found.</div>
                    ) : (
                        artifacts.map((path) => (
                            <button
                                key={path}
                                onClick={() => handleFileClick(path)}
                                className={`w-full text-left flex items-start gap-2 px-3 py-2 rounded-md text-sm transition-colors ${selectedFile === path
                                    ? "bg-primary/10 text-primary font-medium"
                                    : "hover:bg-muted text-muted-foreground hover:text-foreground"
                                    }`}
                            >
                                <FileText className="w-4 h-4 mt-0.5 shrink-0" />
                                <span className="break-all">{path}</span>
                            </button>
                        ))
                    )}
                </div>
            </div>

            <div className="md:col-span-2 bg-card border rounded-lg overflow-hidden flex flex-col">
                <div className="p-3 border-b bg-muted/30 flex justify-between items-center h-[53px]">
                    <div className="font-medium truncate max-w-[300px]" title={selectedFile || ''}>
                        {selectedFile || "Select a file"}
                    </div>
                    {selectedFile && (
                        <button
                            onClick={handleDownload}
                            className="flex items-center gap-1.5 text-xs bg-primary text-primary-foreground px-3 py-1.5 rounded-md hover:bg-primary/90 transition-colors"
                        >
                            <Download className="w-3.5 h-3.5" /> Download
                        </button>
                    )}
                </div>
                <div className="flex-1 overflow-y-auto bg-slate-950 p-4 font-mono text-sm relative">
                    {loadingContent ? (
                        <div className="absolute inset-0 flex items-center justify-center text-muted-foreground">
                            Loading content...
                        </div>
                    ) : selectedFile ? (
                        <pre className="text-slate-50 whitespace-pre-wrap break-words">{content}</pre>
                    ) : (
                        <div className="h-full flex items-center justify-center text-muted-foreground/40">
                            Select a file to view its contents
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
