import React from 'react';

const ResultsDisplay = ({ weavingResult }) => {
  const { status, output, artifacts } = weavingResult;

  return (
    <div className="results-display">
      <h2>Weaving Process Result</h2>
      <div className="status-section">
        <h3>Status: <span className={`status-${status}`}>{status}</span></h3>
      </div>

      {output && (
        <div className="output-section">
          <h3>Generated Output</h3>
          <pre><code>{output}</code></pre>
        </div>
      )}

      {artifacts && artifacts.length > 0 && (
        <div className="artifacts-section">
          <h3>Generated Artifacts</h3>
          <ul>
            {artifacts.map((artifact, index) => (
              <li key={index}>
                <strong>{artifact.name}:</strong>
                <pre><code>{artifact.content}</code></pre>
                <button onClick={() => downloadArtifact(artifact)}>Download</button>
              </li>
            ))}
          </ul>
        </div>
      )}

      {status === 'error' && (
        <div className="error-details">
          <h3>Error Details</h3>
          <p>An error occurred during the weaving process. Please check the logs or contact support.</p>
        </div>
      )}
    </div>
  );
};

const downloadArtifact = (artifact) => {
  const blob = new Blob([artifact.content], { type: 'text/plain' }); // Adjust mime type as needed
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = artifact.name;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
};

export default ResultsDisplay;
