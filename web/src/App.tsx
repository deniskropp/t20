import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Layout } from './components/Layout';
import { Home } from './pages/Home';
import { Run } from './pages/Run';
import { Artifacts } from './pages/Artifacts';

export default function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route element={<Layout />}>
                    <Route path="/" element={<Home />} />
                    <Route path="/artifacts" element={<Artifacts />} />
                    <Route path="/run/:jobId" element={<Run />} />
                </Route>
            </Routes>
        </BrowserRouter>
    );
}
