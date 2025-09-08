import React from 'react';
import './Dashboard.css'; // Assuming shared styles

function CurrentTask({ agentName, task }) {
  return (
    <div className="current-task-item">
      <span className="task-agent-name">{agentName}:</span>
      <span className="task-description">{task}</span>
    </div>
  );
}

export default CurrentTask;
