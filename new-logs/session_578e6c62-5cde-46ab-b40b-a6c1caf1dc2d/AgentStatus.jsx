import React from 'react';
import './Dashboard.css'; // Assuming shared styles

function AgentStatus({ name, status, currentTask }) {
  const getStatusClass = (status) => {
    switch (status.toLowerCase()) {
      case 'active':
        return 'status-active';
      case 'idle':
        return 'status-idle';
      case 'error':
        return 'status-error';
      default:
        return 'status-unknown';
    }
  };

  return (
    <div className="agent-status-card">
      <div className="agent-name">{name}</div>
      <div className={`agent-status ${getStatusClass(status)}`}>{status}</div>
      {currentTask && (
        <div className="agent-task"><strong>Task:</strong> {currentTask}</div>
      )}
    </div>
  );
}

export default AgentStatus;
