import React from 'react';
import './Dashboard.css'; // Assuming shared styles

function Artifacts({ artifacts }) {
  return (
    <ul className="artifacts-list">
      {artifacts.length > 0 ? (
        artifacts.map(artifact => (
          <li key={artifact.id} className="artifact-item">
            <a href={artifact.url} className="artifact-link" target="_blank" rel="noopener noreferrer">
              {artifact.name}
            </a>
            <span className="artifact-type">({artifact.type})</span>
          </li>
        ))
      ) : (
        <p>No artifacts generated yet.</p>
      )}
    </ul>
  );
}

export default Artifacts;
