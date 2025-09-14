import React from 'react';
import ReactDOM from 'react-dom/client';
import Dashboard from './Dashboard';
import './index.css'; // General styles, including font imports

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <Dashboard />
  </React.StrictMode>
);
