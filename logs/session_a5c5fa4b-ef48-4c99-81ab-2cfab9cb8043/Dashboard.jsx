import React, { useState, useEffect } from 'react';
import './Dashboard.css';

// Placeholder for Agent Status Component
const AgentStatus = ({ agents }) => {
  return (
    <section className="agent-status card">
      <h2>Agent Status</h2>
      <div className="agent-list">
        {agents.map(agent => (
          <div key={agent.id} className={`agent-item ${agent.status.toLowerCase()}`}>
            <span className="agent-name">{agent.name}</span>
            <span className="status-indicator"></span>
            <span className="status-text">{agent.status}</span>
          </div>
        ))}
      </div>
    </section>
  );
};

// Placeholder for Current Task Component
const CurrentTask = ({ agents }) => {
  return (
    <section className="current-task card">
      <h2>Current Task</h2>
      <div className="task-list">
        {agents.map(agent => (
          <div key={agent.id} className="task-item">
            <span className="agent-name">{agent.name}:</span>
            <span className="task-description">{agent.currentTask || 'Idle'}</span>
          </div>
        ))}
      </div>
    </section>
  );
};

// Placeholder for Artifacts Component
const Artifacts = ({ agents }) => {
  return (
    <section className="artifacts card">
      <h2>Generated Artifacts</h2>
      <div className="artifact-list">
        {agents.map(agent => (
          <div key={agent.id} className="agent-artifacts">
            <span className="agent-name">{agent.name}:</span>
            <div className="artifact-items">
              {agent.artifacts && agent.artifacts.length > 0 ? (
                agent.artifacts.map((artifact, index) => (
                  <a key={index} href="#" className="artifact-link">{artifact.name}</a>
                ))
              ) : (
                <span>No artifacts yet</span>
              )}
            </div>
          </div>
        ))}
      </div>
    </section>
  );
};

// Placeholder for Log Feed Component
const LogFeed = ({ logs }) => {
  const logContainerRef = React.useRef(null);

  useEffect(() => {
    // Scroll to the bottom when new logs arrive
    if (logContainerRef.current) {
      logContainerRef.current.scrollTop = logContainerRef.current.scrollHeight;
    }
  }, [logs]);

  return (
    <section className="log-feed card">
      <h2>Workflow Log</h2>
      <div ref={logContainerRef} className="log-messages">
        {logs.map((log, index) => (
          <div key={index} className="log-entry">
            <span className="log-timestamp">[{new Date(log.timestamp).toLocaleTimeString()}]</span>
            <span className="log-message">{log.message}</span>
          </div>
        ))}
      </div>
    </section>
  );
};

// Placeholder for Orchestrator Prompts Component
const OrchestratorPrompts = ({ prompt }) => {
  return (
    <section className="orchestrator-prompts card">
      <h2>Next Steps for Orchestrator</h2>
      <p className="prompt-text">{prompt || 'Awaiting instructions...'}</p>
    </section>
  );
};

const Dashboard = () => {
  // Mock data - in a real application, this would come from an API or state management
  const [agents, setAgents] = useState([
    { id: 1, name: 'La Metta', status: 'Active', currentTask: 'Generating ambient textures', artifacts: [{ name: 'ambient_texture_v1.wav' }] },
    { id: 2, name: 'Dima', status: 'Active', currentTask: 'Establishing rhythmic foundation', artifacts: [{ name: 'bassline_loop_01.mid' }] },
    { id: 3, name: 'Kick', status: 'Idle', currentTask: 'Awaiting trigger', artifacts: [] },
    { id: 4, name: 'Fizz', status: 'Active', currentTask: 'Adding percussive sparkle', artifacts: [{ name: 'sparkle_pattern_a.wav' }] },
    { id: 5, name: 'Fozz', status: 'Active', currentTask: 'Developing atmospheric resonance', artifacts: [{ name: 'resonance_pad_v1.fxp' }] },
  ]);

  const [logs, setLogs] = useState([
    { timestamp: Date.now() - 5000, message: 'Workflow initiated.' },
    { timestamp: Date.now() - 3000, message: 'Agent La Metta started task: Generating ambient textures.' },
    { timestamp: Date.now() - 2000, message: 'Agent Dima started task: Establishing rhythmic foundation.' },
    { timestamp: Date.now() - 1000, message: 'Agent Fizz started task: Adding percussive sparkle.' },
  ]);

  const [orchestratorPrompt, setOrchestratorPrompt] = useState('Monitor agent progress and await completion of initial tasks.');

  // Simulate real-time updates (e.g., fetching data every few seconds)
  useEffect(() => {
    const interval = setInterval(() => {
      // Simulate new log entries
      const newLog = {
        timestamp: Date.now(),
        message: `Simulated log entry at ${new Date().toLocaleTimeString()}`,
      };
      setLogs(prevLogs => [...prevLogs, newLog].slice(-50)); // Keep only the last 50 logs

      // Simulate agent status/task updates
      setAgents(prevAgents => {
        const updatedAgents = prevAgents.map(agent => {
          if (agent.id === 1 && agent.status === 'Active' && Math.random() > 0.7) {
            return { ...agent, status: 'Idle', currentTask: 'Completed texture generation' };
          }
          if (agent.id === 2 && agent.status === 'Active' && Math.random() > 0.6) {
             return { ...agent, status: 'Active', currentTask: 'Refining bassline loop' };
          }
          if (agent.id === 3 && agent.status === 'Idle' && Math.random() > 0.5) {
             return { ...agent, status: 'Active', currentTask: 'Executing kick pattern' };
          }
          return agent;
        });
        // Update orchestrator prompt based on agent status
        const allIdleOrCompleted = updatedAgents.every(a => a.status === 'Idle' || a.status === 'Completed');
        if (allIdleOrCompleted) {
          setOrchestratorPrompt('All initial tasks complete. Ready for next loop iteration or refinement.');
        }
        return updatedAgents;
      });

    }, 5000); // Update every 5 seconds

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <h1>'La Metta, Dima, Kick, Fizz and Fozz' - Looping Execution Dashboard</h1>
      </header>
      <main className="dashboard-main">
        <div className="dashboard-grid">
          <AgentStatus agents={agents} />
          <CurrentTask agents={agents} />
          <Artifacts agents={agents} />
          <LogFeed logs={logs} />
        </div>
        <OrchestratorPrompts prompt={orchestratorPrompt} />
      </main>
    </div>
  );
};

export default Dashboard;
