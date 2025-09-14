import React, { useState } from 'react';

const IntegrationMappingInterface = ({ sysSourceData, templateSourceData, onIntegrationComplete }) => {
  const [mapping, setMapping] = useState({});
  const [rules, setRules] = useState([]);
  const [currentRule, setCurrentRule] = useState({ condition: '', action: '' });

  // Mock data for demonstration purposes
  // In a real app, this would come from sysSourceData and templateSourceData props
  const mockSysFields = sysSourceData?.fields || ['sys_id', 'sys_name', 'sys_value', 'sys_timestamp'];
  const mockTemplateFields = templateSourceData?.fields || ['template_id', 'template_name', 'template_data', 'template_date'];

  const handleMappingChange = (sysField, templateField) => {
    setMapping(prev => ({ ...prev, [sysField]: templateField }));
  };

  const handleAddRule = () => {
    if (currentRule.condition && currentRule.action) {
      setRules(prev => [...prev, currentRule]);
      setCurrentRule({ condition: '', action: '' });
    } else {
      alert('Please define both a condition and an action for the rule.');
    }
  };

  const handleRuleChange = (field, value) => {
    setCurrentRule(prev => ({ ...prev, [field]: value }));
  };

  const handleSubmit = () => {
    onIntegrationComplete({ mapping, rules });
  };

  return (
    <div className="integration-mapping-interface">
      <h2>Integration and Weaving Interface</h2>
      
      <div className="mapping-section">
        <h3>Data Mapping</h3>
        <div className="field-columns">
          <div className="sys-fields">
            <h4>SYS Fields</h4>
            {mockSysFields.map(field => (
              <div key={field} className="field-row">
                <span>{field}</span>
                <select
                  onChange={(e) => handleMappingChange(field, e.target.value)}
                  value={mapping[field] || ''}
                >
                  <option value="">-- Map To --</option>
                  {mockTemplateFields.map(tField => (
                    <option key={tField} value={tField}>{tField}</option>
                  ))}
                </select>
              </div>
            ))}
          </div>
          <div className="template-fields">
            <h4>TEMPLATE Fields</h4>
            {mockTemplateFields.map(field => (
              <div key={field} className="field-row">
                <span>{field}</span>
                {/* Display which SYS field maps to this TEMPLATE field, if any */}
                <span>Mapped From: {Object.keys(mapping).find(key => mapping[key] === field) || 'N/A'}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="rules-section">
        <h3>Logic and Rules</h3>
        <div className="rule-form">
          <input
            type="text"
            placeholder="Condition (e.g., sys_value > 100)"
            value={currentRule.condition}
            onChange={(e) => handleRuleChange('condition', e.target.value)}
          />
          <input
            type="text"
            placeholder="Action (e.g., set template_data = 'High Value')"
            value={currentRule.action}
            onChange={(e) => handleRuleChange('action', e.target.value)}
          />
          <button type="button" onClick={handleAddRule}>Add Rule</button>
        </div>
        <h4>Current Rules:</h4>
        <ul>
          {rules.map((rule, index) => (
            <li key={index}>{rule.condition} => {rule.action}</li>
          ))}
        </ul>
      </div>

      <button onClick={handleSubmit}>Start Weaving Process</button>
    </div>
  );
};

export default IntegrationMappingInterface;
