import React, { useState, useEffect, useRef, useCallback } from 'react';
import './Dashboard.css';

// Helper function to get status class for styling
const getStatusClass = (status) => {
  switch (status.toLowerCase()) {
    case 'active': return 'status-active';
    case 'idle': return 'status-idle';
    case 'error': return 'status-error';
    case 'pending': return 'status-pending'; // Added pending status
    case 'completed': return 'status-completed'; // Added completed status
    default: return 'status-unknown';
  }
};

// Component for displaying individual agent status
const AgentStatus = React.memo(({ agentName, status, currentTask }) => {
  return (
    <div className="agent-card" role="listitem" aria-label={`${agentName} status: ${status}. Current task: ${currentTask || 'None'}`}>
      <h3>{agentName}</h3>
      <div className="status-indicator">
        <span className={`status-dot ${getStatusClass(status)}`} aria-hidden="true"></span>
        <span className="status-text">{status.charAt(0).toUpperCase() + status.slice(1)}</span>
      </div>
      {currentTask && (
        <p className="current-task"><strong>Task:</strong> {currentTask}</p>
      )}
    </div>
  );
});

// Component for displaying generated artifacts
const Artifacts = React.memo(({ artifacts }) => {
  const handleArtifactClick = useCallback((e, artifactName) => {
    e.preventDefault();
    // In a real app, this would trigger a download or display.
    alert(`Action: Displaying or downloading artifact: ${artifactName}`);
  }, []);

  return (
    <div className="artifacts-section">
      <h4>Generated Artifacts</h4>
      {artifacts && artifacts.length > 0 ? (
        <ul role="list">
          {artifacts.map((artifact, index) => (
            <li key={index} role="listitem">
              <a href="#" onClick={(e) => handleArtifactClick(e, artifact.name)}>
                {artifact.name}
              </a>
            </li>
          ))}
        </ul>
      ) : (
        <p>No artifacts generated yet.</p>
      )}
    </div>
  );
});

// Component for the real-time log feed
const LogFeed = React.memo(({ logs }) => {
  const logContainerRef = useRef(null);

  // Scroll to the bottom when new logs are added
  useEffect(() => {
    if (logContainerRef.current) {
      logContainerRef.current.scrollTop = logContainerRef.current.scrollHeight;
    }
  }, [logs]);

  return (
    <div className="log-feed-container">
      <h4>Real-time Log Feed</h4>
      <div className="log-messages" ref={logContainerRef} role="log" aria-live="polite">
        {logs.length > 0 ? (
          logs.map((log, index) => (
            <p key={index} className={`log-entry log-${log.level}`}>
              <span className="log-timestamp">[{new Date(log.timestamp).toLocaleTimeString()}]</span>
              <span className="log-message" id={`log-${index}`}>{log.message}</span>
            </p>
          ))
        ) : (
          <p>No logs yet.</p>
        )}
      </div>
    </div>
  );
});

// Component for displaying orchestrator prompts/next steps
const OrchestratorPrompts = React.memo(({ prompt }) => {
  return (
    <div className="orchestrator-prompt-section">
      <h4>Next Step for Orchestrator</h4>
      <p>{prompt || 'Awaiting instructions...'}</p>
    </div>
  );
});

const Dashboard = () => {
  // Mock data - In a real app, this state would be managed via context, Redux, or fetched from an API.
  const [agents, setAgents] = useState([
    { id: 1, name: 'La Metta', status: 'active', currentTask: 'Processing input data' },
    { id: 2, name: 'Dima', status: 'idle', currentTask: null },
    { id: 3, name: 'Kick', status: 'active', currentTask: 'Generating intermediate results' },
    { id: 4, name: 'Fizz', status: 'error', currentTask: 'Failed to connect to service' },
    { id: 5, name: 'Fozz', status: 'pending', currentTask: 'Awaiting validation input' },
  ]);

  const [artifacts, setArtifacts] = useState([
    { name: 'intermediate_results.json' },
    { name: 'validation_report.pdf' },
  ]);

  const [logs, setLogs] = useState([
    { timestamp: Date.now() - 5000, level: 'info', message: 'La Metta started processing input data.' },
    { timestamp: Date.now() - 3000, level: 'info', message: 'Kick started generating intermediate results.' },
    { timestamp: Date.now() - 1000, level: 'error', message: 'Fizz encountered an error: Failed to connect to service.' },
    { timestamp: Date.now(), level: 'info', message: 'La Metta finished processing input data.' },
  ]);

  const [orchestratorPrompt, setOrchestratorPrompt] = useState('Review Fizz agent status and decide on next action.');
  const [globalStatus, setGlobalStatus] = useState('Active'); // Example global status

  // Simulate real-time updates for demonstration purposes
  const simulationIntervalRef = useRef(null);

  const simulateUpdates = useCallback(() => {
    setAgents(prevAgents =>
      prevAgents.map(agent => {
        // Simulate status changes for idle/pending agents
        if ((agent.id === 2 && agent.status === 'idle' && Math.random() > 0.4) || (agent.id === 5 && agent.status === 'pending' && Math.random() > 0.6)) {
          return { ...agent, status: 'active', currentTask: 'Receiving data' };
        }
        // Simulate task completion
        if (agent.status === 'active' && Math.random() > 0.7) {
          const completedTask = agent.currentTask;
          const updatedAgent = { ...agent, status: 'completed', currentTask: null };
          // Add a log for task completion
          setLogs(prevLogs => [
            ...prevLogs.slice(-99), // Keep last 100 logs
            { timestamp: Date.now(), level: 'info', message: `${agent.name} completed task: ${completedTask}` },
          ]);
          return updatedAgent;
        }
        return agent;
      })
    );

    // Simulate new log entry
    const newLog = {
      timestamp: Date.now(),
      level: Math.random() > 0.8 ? 'warn' : (Math.random() > 0.95 ? 'error' : 'info'),
      message: `Simulated log entry at ${new Date().toLocaleTimeString()}`,
    };
    setLogs(prevLogs => [...prevLogs.slice(-99), newLog]); // Keep only last 100 logs

    // Simulate prompt change
    if (Math.random() > 0.85) {
      setOrchestratorPrompt('Consider restarting the Fizz agent or re-routing its task.');
    }
     // Simulate global status change
    if (Math.random() > 0.9) {
       setGlobalStatus(prevStatus => prevStatus === 'Active' ? 'Paused' : 'Active');
    }
  }, [setLogs, setAgents, setOrchestratorPrompt, setGlobalStatus]);

  useEffect(() => {
    simulationIntervalRef.current = setInterval(simulateUpdates, 7000); // Update every 7 seconds
    // Initial update on mount
    simulateUpdates();

    return () => clearInterval(simulationIntervalRef.current); // Cleanup on component unmount
  }, [simulateUpdates]); // Dependency array includes the function itself

  return (
    <div className="dashboard-container" aria-labelledby="dashboard-title">
      <header className="dashboard-header">
        <div className="logo" id="dashboard-logo">LDKFF</div> {/* Minimalist Logo Placeholder */}
        <h1 id="dashboard-title">Workflow Dashboard</h1>
        <div className="global-status" aria-label={`Overall status: ${globalStatus}`}>Overall: {globalStatus}</div> {/* Minimalist Status */}
      </header>

      <main className="dashboard-main">
        <section className="agents-section">
          <h2 id="agents-title">Agent Status</h2>
          <div className="agents-grid" role="list" aria-labelledby="agents-title">
            {agents.map(agent => (
              <AgentStatus
                key={agent.id}
                agentName={agent.name}
                status={agent.status}
                currentTask={agent.currentTask}
              />
            ))}
          </div>
        </section>

        <section className="details-section">
          <h2 id="details-title">Process Details</h2>
          <div className="details-grid" aria-labelledby="details-title">
            <Artifacts artifacts={artifacts} />
            <OrchestratorPrompts prompt={orchestratorPrompt} />
          </div>
        </section>

        <section className="log-section">
          <LogFeed logs={logs} />
        </section>
      </main>
    </div>
  );
};

export default Dashboard;
