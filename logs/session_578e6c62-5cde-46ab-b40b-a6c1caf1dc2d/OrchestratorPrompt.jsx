import React from 'react';
import './Dashboard.css'; // Assuming shared styles

function OrchestratorPrompt({ prompt }) {
  return (
    <div className="orchestrator-prompt-card">
      <div className="prompt-next-step">
        <strong>Next Step:</strong> {prompt.nextStep}
      </div>
      {prompt.guidance && (
        <div className="prompt-guidance">
          <strong>Guidance:</strong> {prompt.guidance}
        </div>
      )}
    </div>
  );
}

export default OrchestratorPrompt;
