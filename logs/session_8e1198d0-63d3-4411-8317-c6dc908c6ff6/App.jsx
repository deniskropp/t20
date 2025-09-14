import React from 'react';
import './App.css';
import Navigation from './components/Navigation';
import HeroSection from './components/HeroSection';
import ProjectsSection from './components/ProjectsSection';
import Footer from './components/Footer';

function App() {
  return (
    <div className="App">
      <Navigation />
      <main>
        <HeroSection />
        <ProjectsSection />
      </main>
      <Footer />
    </div>
  );
}

export default App;
