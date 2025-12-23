import { useState, useEffect, useMemo } from 'react';
import {
    FileText,
    Download,
    Folder,
    FolderOpen,
    Loader2,
    ChevronRight,
    Code2,
    Image as ImageIcon,
    FileCode,
    Search,
    ZoomIn,
    ZoomOut,
    Archive
} from 'lucide-react';
import { getArtifactContent, getRunState } from '../api';
import { motion, AnimatePresence } from 'framer-motion';
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';
import JSZip from 'jszip';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';

function cn(...inputs: (string | undefined | null | false)[]) {
    return twMerge(clsx(inputs));
}

// --- Types ---
interface ArtifactBrowserProps {
    artifacts?: string[];
    jobId?: string;
}

interface FileNode {
    name: string;
    path: string;
    type: 'file' | 'folder';
    children?: Record<string, FileNode>;
    content?: string;
}

// --- Icons ---
const getFileIcon = (fileName: string) => {
    const ext = fileName.split('.').pop()?.toLowerCase();
    switch (ext) {
        case 'png':
        case 'jpg':
        case 'jpeg':
        case 'gif':
        case 'svg':
            return <ImageIcon className="w-4 h-4 text-purple-400" />;
        case 'md':
        case 'txt':
            return <FileText className="w-4 h-4 text-slate-400" />;
        case 'ts':
        case 'tsx':
        case 'js':
        case 'jsx':
            return <FileCode className="w-4 h-4 text-blue-400" />;
        case 'py':
            return <FileCode className="w-4 h-4 text-yellow-400" />;
        case 'json':
        case 'yaml':
        case 'yml':
            return <Code2 className="w-4 h-4 text-green-400" />;
        default:
            return <FileText className="w-4 h-4 text-slate-500" />;
    }
};

const getLanguage = (fileName: string) => {
    const ext = fileName.split('.').pop()?.toLowerCase();
    switch (ext) {
        case 'ts':
        case 'tsx':
            return 'typescript';
        case 'js':
        case 'jsx':
            return 'javascript';
        case 'py':
            return 'python';
        case 'json':
            return 'json';
        case 'css':
            return 'css';
        case 'html':
            return 'html';
        case 'md':
            return 'markdown';
        case 'yaml':
        case 'yml':
            return 'yaml';
        case 'sh':
        case 'bash':
            return 'bash';
        default:
            return 'text';
    }
};

// --- Component ---
export function ArtifactBrowser({ artifacts: propArtifacts, jobId }: ArtifactBrowserProps) {
    const [selectedPath, setSelectedPath] = useState<string | null>(null);
    const [fileContentMap, setFileContentMap] = useState<Record<string, string>>({});
    const [loadingState, setLoadingState] = useState(false);
    const [loadingContent, setLoadingContent] = useState(false);
    const [searchTerm, setSearchTerm] = useState('');

    // View Settings
    const [fontSize, setFontSize] = useState(13);
    const [downloadingZip, setDownloadingZip] = useState(false);

    // Load Data
    useEffect(() => {
        if (jobId) {
            loadRunState(jobId);
        } else if (propArtifacts) {
            // Legacy mode: just list of paths
            const map: Record<string, string> = {};
            setFileContentMap(map);
        }
    }, [jobId, propArtifacts]);

    const loadRunState = async (id: string) => {
        setLoadingState(true);
        try {
            const state = await getRunState(id);
            const newMap: Record<string, string> = {};

            state.executionLog.forEach(item => {
                if (item.result && item.result.artifact && item.result.artifact.files) {
                    item.result.artifact.files.forEach(file => {
                        newMap[file.path] = file.content;
                    });
                }
            });
            setFileContentMap(newMap);

            // Auto-select first file if available
            const paths = Object.keys(newMap).sort();
            if (paths.length > 0) setSelectedPath(paths[0]);

        } catch (e) {
            console.error("Failed to load run state", e);
        } finally {
            setLoadingState(false);
        }
    };

    // Build File Tree (Memoized)
    const fileTree = useMemo(() => {
        const root: Record<string, FileNode> = {};
        const paths = propArtifacts || Object.keys(fileContentMap);

        // Filter by search
        const filteredPaths = searchTerm
            ? paths.filter(p => p.toLowerCase().includes(searchTerm.toLowerCase()))
            : paths;

        filteredPaths.forEach(path => {
            const parts = path.split('/');
            let current = root;

            parts.forEach((part, index) => {
                if (!current[part]) {
                    current[part] = {
                        name: part,
                        path: parts.slice(0, index + 1).join('/'),
                        type: index === parts.length - 1 ? 'file' : 'folder',
                        children: {}
                    };
                }
                if (index === parts.length - 1) {
                    current[part].type = 'file';
                } else {
                    current = current[part].children!;
                }
            });
        });
        return root;
    }, [fileContentMap, propArtifacts, searchTerm]);

    // Handle Selection
    const handleFileSelect = async (path: string) => {
        setSelectedPath(path);

        // If content is not in map (legacy mode), fetch it
        if (!fileContentMap[path]) {
            setLoadingContent(true);
            try {
                const data = await getArtifactContent(path);
                const contentStr = typeof data === 'string' ? data : JSON.stringify(data, null, 2);
                setFileContentMap(prev => ({ ...prev, [path]: contentStr }));
            } catch (e) {
                console.error("Failed to load content", e);
            } finally {
                setLoadingContent(false);
            }
        }
    };

    const handleDownloadFile = () => {
        if (!selectedPath || !fileContentMap[selectedPath]) return;
        const blob = new Blob([fileContentMap[selectedPath]], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = selectedPath.split('/').pop() || 'artifact';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    };

    const handleDownloadZip = async () => {
        setDownloadingZip(true);
        try {
            const zip = new JSZip();
            // Add all files available in the map
            Object.entries(fileContentMap).forEach(([path, content]) => {
                zip.file(path, content);
            });

            const content = await zip.generateAsync({ type: "blob" });
            const url = URL.createObjectURL(content);
            const a = document.createElement('a');
            a.href = url;
            a.download = `artifacts-${jobId || 'archive'}.zip`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        } catch (e) {
            console.error("Failed to generate zip", e);
        } finally {
            setDownloadingZip(false);
        }
    };

    // Rendering Helpers
    const currentContent = selectedPath ? fileContentMap[selectedPath] : null;
    const isImage = selectedPath?.match(/\.(png|jpg|jpeg|gif|svg)$/i);
    const language = selectedPath ? getLanguage(selectedPath) : 'text';

    if (loadingState) {
        return (
            <div className="h-[75vh] flex items-center justify-center bg-[#1e1e1e] rounded-xl border border-[#333]">
                <Loader2 className="w-8 h-8 animate-spin text-zinc-500" />
            </div>
        );
    }

    return (
        <div className="flex h-[75vh] bg-[#1e1e1e] border border-[#333] rounded-xl overflow-hidden text-[#d4d4d4] font-sans shadow-2xl">
            {/* Sidebar: File Explorer */}
            <div className="w-64 bg-[#252526] flex flex-col border-r border-[#333] shrink-0">
                <div className="p-3 border-b border-[#333] flex items-center justify-between">
                    <span className="text-xs font-bold tracking-wider uppercase text-zinc-500">Explorer</span>
                    <button
                        onClick={handleDownloadZip}
                        disabled={downloadingZip || Object.keys(fileContentMap).length === 0}
                        title="Download All as ZIP"
                        className="text-zinc-500 hover:text-white disabled:opacity-50 transition-colors"
                    >
                        {downloadingZip ? <Loader2 className="w-4 h-4 animate-spin" /> : <Archive className="w-4 h-4" />}
                    </button>
                </div>
                {/* Search */}
                <div className="px-2 py-2 border-b border-[#333]">
                    <div className="relative">
                        <Search className="absolute left-2 top-2 w-3.5 h-3.5 text-zinc-500" />
                        <input
                            type="text"
                            placeholder="Search..."
                            value={searchTerm}
                            onChange={e => setSearchTerm(e.target.value)}
                            className="w-full bg-[#1e1e1e] border border-[#333] pl-7 pr-2 py-1 text-xs rounded text-zinc-300 focus:outline-none focus:border-blue-500/50"
                        />
                    </div>
                </div>

                <div className="flex-1 overflow-y-auto p-2 custom-scrollbar">
                    {Object.keys(fileTree).length === 0 ? (
                        <div className="text-xs text-zinc-500 text-center py-4">No artifacts found.</div>
                    ) : (
                        <FileTree
                            nodes={fileTree}
                            selectedPath={selectedPath}
                            onSelect={handleFileSelect}
                        />
                    )}
                </div>
            </div>

            {/* Main: Content Preview */}
            <div className="flex-1 flex flex-col min-w-0 bg-[#1e1e1e]">
                {/* Tab Header */}
                <div className="h-9 bg-[#2d2d2d] flex items-center border-b border-[#333] overflow-x-auto custom-scrollbar no-scrollbar">
                    {selectedPath ? (
                        <div className="px-3 py-1.5 bg-[#1e1e1e] border-t-2 border-t-blue-500 text-sm flex items-center gap-2 border-r border-[#333] min-w-[120px]">
                            {getFileIcon(selectedPath)}
                            <span className="truncate max-w-[200px]">{selectedPath.split('/').pop()}</span>
                        </div>
                    ) : (
                        <div className="px-4 text-xs italic text-zinc-600">No file selected</div>
                    )}
                </div>

                {/* Toolbar */}
                {selectedPath && (
                    <div className="px-4 py-2 border-b border-[#333] flex items-center justify-between text-xs bg-[#1e1e1e]">
                        <div className="text-zinc-500 truncate select-all">{selectedPath}</div>
                        <div className="flex items-center gap-4">
                            {!isImage && (
                                <div className="flex items-center gap-1 bg-[#2d2d2d] rounded-md border border-[#333] p-0.5">
                                    <button
                                        onClick={() => setFontSize(Math.max(6, fontSize - 1))}
                                        className="p-1 hover:bg-[#333] rounded text-zinc-400 hover:text-white"
                                        title="Decrease font size"
                                    >
                                        <ZoomOut className="w-3.5 h-3.5" />
                                    </button>
                                    <span className="text-[10px] min-w-[2ch] text-center text-zinc-500">{fontSize}</span>
                                    <button
                                        onClick={() => setFontSize(Math.min(24, fontSize + 1))}
                                        className="p-1 hover:bg-[#333] rounded text-zinc-400 hover:text-white"
                                        title="Increase font size"
                                    >
                                        <ZoomIn className="w-3.5 h-3.5" />
                                    </button>
                                </div>
                            )}
                            <button
                                onClick={handleDownloadFile}
                                className="flex items-center gap-1.5 hover:text-white transition-colors"
                            >
                                <Download className="w-3.5 h-3.5" /> Download
                            </button>
                        </div>
                    </div>
                )}

                {/* Editor/Viewer */}
                <div className="flex-1 overflow-auto relative custom-scrollbar bg-[#1e1e1e]">
                    {loadingContent ? (
                        <div className="absolute inset-0 flex items-center justify-center text-zinc-500">
                            <Loader2 className="w-6 h-6 animate-spin mb-2" />
                            <span className="text-sm">Loading...</span>
                        </div>
                    ) : selectedPath ? (
                        isImage && currentContent ? (
                            <div className="min-h-full flex items-center justify-center bg-[#151515] p-8">
                                <img src={`data:image/png;base64,${currentContent}`} alt="Preview" className="max-w-full max-h-full shadow-lg rounded" />
                            </div>
                        ) : (
                            <div className="flex min-h-full text-[13px] leading-relaxed">
                                {/* Syntax Highlighter */}
                                <div className="flex-1 min-w-0">
                                    <SyntaxHighlighter
                                        language={language}
                                        style={vscDarkPlus}
                                        customStyle={{
                                            margin: 0,
                                            padding: '1.5rem',
                                            background: 'transparent',
                                            fontSize: `${fontSize}px`,
                                            lineHeight: '1.5',
                                        }}
                                        codeTagProps={{
                                            style: { fontSize: 'inherit' }
                                        }}
                                        showLineNumbers={true}
                                        lineNumberStyle={{
                                            color: '#6e7681',
                                            paddingRight: '1rem',
                                            textAlign: 'right',
                                            minWidth: '3.5em'
                                        }}
                                    >
                                        {currentContent || ''}
                                    </SyntaxHighlighter>
                                </div>
                            </div>
                        )
                    ) : (
                        <div className="h-full flex flex-col items-center justify-center text-zinc-600 gap-3">
                            <Code2 className="w-16 h-16 opacity-20" />
                            <p className="text-sm">Select a file to view its content</p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}

// --- Recursive File Tree Component ---
function FileTree({ nodes, selectedPath, onSelect }: { nodes: Record<string, FileNode>, selectedPath: string | null, onSelect: (p: string) => void }) {
    // Sort: Folders first, then files, alphabetically
    const sortedKeys = Object.keys(nodes).sort((a, b) => {
        const nodeA = nodes[a];
        const nodeB = nodes[b];
        if (nodeA.type === nodeB.type) return a.localeCompare(b);
        return nodeA.type === 'folder' ? -1 : 1;
    });

    return (
        <div className="pl-1">
            {sortedKeys.map(key => (
                <FileTreeItem
                    key={key}
                    node={nodes[key]}
                    selectedPath={selectedPath}
                    onSelect={onSelect}
                />
            ))}
        </div>
    );
}

function FileTreeItem({ node, selectedPath, onSelect }: { node: FileNode, selectedPath: string | null, onSelect: (p: string) => void }) {
    const isFolder = node.type === 'folder';
    const [isOpen, setIsOpen] = useState(false);

    // Auto-open if selected path is inside this folder
    useEffect(() => {
        if (selectedPath && selectedPath.startsWith(node.path + '/')) {
            setIsOpen(true);
        }
    }, [selectedPath, node.path]);

    const handleSelect = () => {
        if (isFolder) {
            setIsOpen(!isOpen);
        } else {
            onSelect(node.path);
        }
    };

    return (
        <div>
            <div
                onClick={handleSelect}
                className={cn(
                    "flex items-center gap-1.5 py-1 px-2 rounded cursor-pointer text-[13px] select-none transition-colors",
                    selectedPath === node.path
                        ? "bg-blue-500/20 text-blue-400"
                        : "hover:bg-white/5 text-zinc-400 hover:text-zinc-200"
                )}
            >
                <div className="opacity-70 shrink-0 w-3.5 text-center flex items-center justify-center">
                    {isFolder ? (
                        <ChevronRight className={cn("w-3 h-3 transition-transform", isOpen && "rotate-90")} />
                    ) : (
                        <span className="w-3" />
                    )}
                </div>

                <div className="shrink-0 text-yellow-500/80">
                    {isFolder ? (
                        isOpen ? <FolderOpen className="w-3.5 h-3.5" /> : <Folder className="w-3.5 h-3.5" />
                    ) : (
                        getFileIcon(node.name)
                    )}
                </div>

                <span className="truncate">{node.name}</span>
            </div>

            <AnimatePresence>
                {isFolder && isOpen && node.children && (
                    <motion.div
                        initial={{ height: 0, opacity: 0 }}
                        animate={{ height: "auto", opacity: 1 }}
                        exit={{ height: 0, opacity: 0 }}
                        className="overflow-hidden border-l border-white/5 ml-[1.1rem]"
                    >
                        <FileTree nodes={node.children} selectedPath={selectedPath} onSelect={onSelect} />
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
}

// Add global style for scrollbar if not exists (dup of console but safer)
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
.no-scrollbar::-webkit-scrollbar {
    display: none;
}
`;
document.head.appendChild(style);
