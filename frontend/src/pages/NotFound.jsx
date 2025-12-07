import React from 'react';
import { Link } from 'react-router-dom';
import { AlertTriangle, Home, RefreshCw } from 'lucide-react';
import './NotFound.css';

const NotFound = () => {
  return (
    <div className="page-404">
      <div className="error-container">
        <div className="glitch-wrapper">
          <h1 className="glitch" data-text="404">404</h1>
        </div>
        
        <div className="error-content animate-fade-in">
          <div className="error-badge">
            <AlertTriangle size={16} /> SYSTEM FAILURE
          </div>
          
          <h2>Pipeline Deployment Failed.</h2>
          <p>
            Bro, you took a wrong turn in the deployment pipeline. 
            The resource you are looking for has been de-provisioned or never existed.
          </p>

          <div className="error-actions">
            <Link to="/" className="btn-primary-glow">
              <Home size={18} /> Rollback to Home
            </Link>
            <button onClick={() => window.location.reload()} className="btn-outline">
              <RefreshCw size={18} /> Retry Build
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default NotFound;