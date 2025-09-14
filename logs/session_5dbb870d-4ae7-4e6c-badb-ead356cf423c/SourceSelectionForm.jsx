import React, { useState } from 'react';

const SourceSelectionForm = ({ onSourceConfigured }) => {
  const [sysSource, setSysSource] = useState({ type: '', config: {} });
  const [templateSource, setTemplateSource] = useState({ type: '', config: {} });
  const [connectionStatus, setConnectionStatus] = useState({});

  const handleSourceChange = (sourceType, field, value) => {
    if (sourceType === 'sys') {
      setSysSource(prev => ({ ...prev, [field]: value }));
    } else {
      setTemplateSource(prev => ({ ...prev, [field]: value }));
    }
  };

  const handleConfigChange = (sourceType, configField, value) => {
    if (sourceType === 'sys') {
      setSysSource(prev => ({ ...prev, config: { ...prev.config, [configField]: value } }));
    } else {
      setTemplateSource(prev => ({ ...prev, config: { ...prev.config, [configField]: value } }));
    }
  };

  const testConnection = async (sourceType) => {
    const source = sourceType === 'sys' ? sysSource : templateSource;
    console.log(`Testing connection for ${sourceType} source...`, source);
    // Mock API call to test connection
    setConnectionStatus(prev => ({ ...prev, [sourceType]: 'testing' }));
    await new Promise(resolve => setTimeout(resolve, 1000)); // Simulate network latency
    const isConnected = Math.random() > 0.2; // Simulate success/failure
    setConnectionStatus(prev => ({ ...prev, [sourceType]: isConnected ? 'connected' : 'error' }));
    if (isConnected) {
      console.log(`${sourceType} connection successful.`);
    } else {
      console.error(`${sourceType} connection failed.`);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (connectionStatus.sys === 'connected' && connectionStatus.template === 'connected') {
      onSourceConfigured({ sysSource, templateSource });
    } else {
      alert('Please ensure both sources are connected successfully before proceeding.');
    }
  };

  const renderSourceForm = (sourceType, sourceState) => (
    <div className={`source-config-section ${sourceType}`}>
      <h3>{sourceType === 'sys' ? 'SYS Source' : 'TEMPLATE Source'}</h3>
      <label htmlFor={`${sourceType}-type`}>Source Type:</label>
      <select
        id={`${sourceType}-type`}
        value={sourceState.type}
        onChange={(e) => handleSourceChange(sourceType, 'type', e.target.value)}
      >
        <option value="">Select Type</option>
        <option value="api">API</option>
        <option value="file">File</option>
        <option value="database">Database</option>
      </select>

      {sourceState.type === 'api' && (
        <div>
          <label htmlFor={`${sourceType}-api-url`}>API URL:</label>
          <input
            type="text"
            id={`${sourceType}-api-url`}
            value={sourceState.config.url || ''}
            onChange={(e) => handleConfigChange(sourceType, 'url', e.target.value)}
          />
          <label htmlFor={`${sourceType}-api-key`}>API Key (Optional):</label>
          <input
            type="password"
            id={`${sourceType}-api-key`}
            value={sourceState.config.apiKey || ''}
            onChange={(e) => handleConfigChange(sourceType, 'apiKey', e.target.value)}
          />
        </div>
      )}
      {sourceState.type === 'file' && (
        <div>
          <label htmlFor={`${sourceType}-file-path`}>File Path:</label>
          <input
            type="text"
            id={`${sourceType}-file-path`}
            value={sourceState.config.path || ''}
            onChange={(e) => handleConfigChange(sourceType, 'path', e.target.value)}
          />
        </div>
      )}
      {sourceState.type === 'database' && (
        <div>
          <label htmlFor={`${sourceType}-db-connection-string`}>Connection String:</label>
          <input
            type="text"
            id={`${sourceType}-db-connection-string`}
            value={sourceState.config.connectionString || ''}
            onChange={(e) => handleConfigChange(sourceType, 'connectionString', e.target.value)}
          />
        </div>
      )}

      <button type="button" onClick={() => testConnection(sourceType)} disabled={!sourceState.type}>
        Test Connection
      </button>
      {connectionStatus[sourceType] && (
        <span className={`connection-status ${connectionStatus[sourceType]}`}>
          {connectionStatus[sourceType] === 'connected' ? '✅ Connected' : connectionStatus[sourceType] === 'error' ? '❌ Error' : 'Testing...'}
        </span>
      )}
    </div>
  );

  return (
    <form onSubmit={handleSubmit} className="source-selection-form">
      <h2>Source Configuration</h2>
      {renderSourceForm('sys', sysSource)}
      {renderSourceForm('template', templateSource)}
      <button type="submit" disabled={!sysSource.type || !templateSource.type || connectionStatus.sys !== 'connected' || connectionStatus.template !== 'connected'}>
        Configure Integration
      </button>
    </form>
  );
};

export default SourceSelectionForm;
