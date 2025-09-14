import React from 'react';
import AgentStatus from './AgentStatus';
import CurrentTask from './CurrentTask';
import Artifacts from './Artifacts';
import LogFeed from './LogFeed';
import OrchestratorPrompt from './OrchestratorPrompt';
import './Dashboard.css'; // Assuming CSS will be imported here or handled by a CSS-in-JS solution

function Dashboard() {
  // Placeholder for state and data fetching logic
  const agentData = [
    { id: 1, name: 'Agent Alpha', status: 'active', task: 'Processing data batch X' },
    { id: 2, name: 'Agent Beta', status: 'idle', task: null },
    { id: 3, name: 'Agent Gamma', status: 'error', task: 'Failed to connect to API' },
  ];

  const artifacts = [
    { id: 'art1', name: 'Report_Q1.pdf', url: '#', type: 'report' },
    { id: 'art2', name: 'Data_Summary.csv', url: '#', type: 'data' },
  ];

  const logs = [
    { id: 'log1', timestamp: '2023-10-27T10:00:00Z', message: 'Agent Alpha started task Processing data batch X.' },
    { id: 'log2', timestamp: '2023-10-27T10:05:15Z', message: 'Agent Gamma encountered an error: Failed to connect to API.' },
    { id: 'log3', timestamp: '2023-10-27T10:10:30Z', message: 'Agent Alpha completed processing data batch X.' },
  ];

  const orchestratorPrompt = {
    nextStep: 'Review Agent Gamma logs and re-initiate task.',
    guidance: 'Ensure network connectivity before retrying.'
  };

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        {/* Logo could go here, or it might be part of a larger layout */} 
        <h1 className="dashboard-title">Dimas Realm Dashboard</h1>
      </header>
      <main className="dashboard-main">
        <div className="dashboard-section agent-status-section">
          <h2 className="section-title">Agent Status</h2>
          <div className="agent-list">
            {agentData.map(agent => (
              <AgentStatus key={agent.id} name={agent.name} status={agent.status} currentTask={agent.task} />
            ))}
          </div>
        </div>

        <div className="dashboard-section current-task-section">
          <h2 className="section-title">Current Task</h2>
          <div className="task-list">
            {agentData.filter(agent => agent.status === 'active').map(agent => (
              <CurrentTask key={agent.id} agentName={agent.name} task={agent.task} />
            ))}
            {agentData.filter(agent => agent.status === 'active').length === 0 && <p>No agents are currently active.</p>}
          </div>
        </div>

        <div className="dashboard-section artifacts-section">
          <h2 className="section-title">Generated Artifacts</h2>
          <Artifacts artifacts={artifacts} />
        </div>

        <div className="dashboard-section log-feed-section">
          <h2 className="section-title">Workflow Log</h2>
          <LogFeed logs={logs} />
        </div>

        <div className="dashboard-section orchestrator-prompt-section">
          <h2 className="section-title">Orchestrator Guidance</h2>
          <OrchestratorPrompt prompt={orchestratorPrompt} />
        </div>
      </main>
    </div>
  );
}

export default Dashboard;
