import { Link, Outlet } from 'react-router-dom';
import { Layers } from 'lucide-react';

export function Layout() {
    return (
        <div className="min-h-screen bg-background font-sans antialiased text-foreground">
            <header className="border-b bg-card/50 backdrop-blur sticky top-0 z-50">
                <div className="container mx-auto px-4 h-16 flex items-center justify-between">
                    <Link to="/" className="flex items-center gap-2 font-bold text-xl text-primary">
                        <Layers className="w-6 h-6" />
                        <span>T20 Runtime</span>
                    </Link>
                    <nav className="flex items-center gap-4">
                        <Link to="/" className="text-sm font-medium hover:text-primary transition-colors">New Task</Link>
                        <Link to="/runs" className="text-sm font-medium hover:text-primary transition-colors">Runs</Link>
                        <Link to="/artifacts" className="text-sm font-medium hover:text-primary transition-colors">Artifacts</Link>
                    </nav>
                </div>
            </header>
            <main className="container mx-auto px-4 py-8">
                <Outlet />
            </main>
        </div>
    );
}
