import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { CheckCircle, AlertTriangle, Server, Database, Activity, GitCommit } from 'lucide-react';
import './Status.css';

const Status = () => {
  const [status, setStatus] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const checkSystem = async () => {
      try {
        const response = await api.get('/features/status/');
        setStatus(response.data);
      } catch (error) {
        setStatus({ status: 'Outage', services: [] });
      } finally {
        setLoading(false);
      }
    };
    checkSystem();
  }, []);

  if (loading) return <div className="status-loading">Pinging Systems...</div>;

  const isOperational = status?.status === 'Operational';

  return (
    <div className="page-status">
      <div className="status-header">
        <h1 className="page-title">System <span className="highlight">Health</span></h1>
        <p className="page-subtitle">Real-time operational status of all services.</p>
      </div>

      {/* Main Banner */}
      <div className={`status-banner ${isOperational ? 'good' : 'bad'} animate-fade-in`}>
        {isOperational ? <CheckCircle size={32} /> : <AlertTriangle size={32} />}
        <div>
            <h2>{isOperational ? 'All Systems Operational' : 'System Degraded'}</h2>
            <p>Last updated: {new Date().toLocaleTimeString()}</p>
        </div>
      </div>

      {/* Metrics Grid */}
      <div className="metrics-grid">
        <div className="metric-card">
            <div className="metric-label"><Activity size={16}/> API Latency</div>
            <div className="metric-value" style={{color: 'var(--neon-green)'}}>{status?.latency || '0ms'}</div>
        </div>
        <div className="metric-card">
            <div className="metric-label"><GitCommit size={16}/> Current Version</div>
            <div className="metric-value">{status?.version || 'v1.0.0'}</div>
        </div>
        <div className="metric-card">
            <div className="metric-label"><Server size={16}/> Region</div>
            <div className="metric-value">{status?.region || 'Localhost'}</div>
        </div>
      </div>

      {/* Services List */}
      <div className="services-list">
        <h3>Component Status</h3>
        <div className="service-row">
            <div className="service-name"><Database size={16}/> Main Database (PostgreSQL)</div>
            <div className="service-status good">{status?.database}</div>
        </div>
        
        {status?.services?.map((svc, i) => (
            <div key={i} className="service-row">
                <div className="service-name">{svc.name}</div>
                <div className="service-status good">Operational</div>
            </div>
        ))}
      </div>
    </div>
  );
};

export default Status;