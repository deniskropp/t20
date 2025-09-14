import React, { useEffect, useRef } from 'react';
import './Dashboard.css'; // Assuming shared styles

function LogFeed({ logs }) {
  const logEndRef = useRef(null);

  // Auto-scroll to the bottom when logs update
  useEffect(() => {
    logEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [logs]);

  const formatTimestamp = (timestamp) => {
    // Basic formatting, can be improved with a date library
    return new Date(timestamp).toLocaleString();
  };

  return (
    <div className="log-feed-container">
      {logs.length > 0 ? (
        <ul className="log-list">
          {logs.map(log => (
            <li key={log.id} className="log-item">
              <span className="log-timestamp">[{formatTimestamp(log.timestamp)}]</span>
              <span className="log-message">{log.message}</span>
            </li>
          ))}
        </ul>
      ) : (
        <p>No logs available.</p>
      )}
      <div ref={logEndRef} /> {/* Element to scroll to */} 
    </div>
  );
}

export default LogFeed;
