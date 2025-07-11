import React from 'react';
import ReactDOM from 'react-dom/client';
import './style.css';
import DashboardPage from './DashboardPage';

ReactDOM.createRoot(document.getElementById('app') as HTMLElement).render(
  <React.StrictMode>
    <DashboardPage />
  </React.StrictMode>
);
