import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Layout } from './components/Layout';
import { Home } from './pages/Home';
import { Run } from './pages/Run';
import { Runs } from './pages/Runs';
import { Artifacts } from './pages/Artifacts';
import { DesignPage } from './pages/DesignPage';
import { TeamPage } from './pages/TeamPage';
import { PlanPage } from './pages/PlanPage';
import { PlanProvider } from './context/PlanContext';

export default function App() {
    return (
        <PlanProvider>
            <BrowserRouter>
                <Routes>
                    <Route element={<Layout />}>
                        <Route path="/" element={<Home />} />
                        <Route path="/design" element={<DesignPage />} />
                        <Route path="/team" element={<TeamPage />} />
                        <Route path="/plan" element={<PlanPage />} />
                        <Route path="/runs" element={<Runs />} />
                        <Route path="/artifacts" element={<Artifacts />} />
                        <Route path="/run/:jobId" element={<Run />} />
                    </Route>
                </Routes>
            </BrowserRouter>
        </PlanProvider>
    );
}
