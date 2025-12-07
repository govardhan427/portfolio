import React from 'react';
import './BuilderStatement.css';

const BuilderStatement = () => {
  return (
    <div className="builder-statement">
      <div className="sentence-container">
        <span className="static-text">I</span>
        
        <div className="word-carousel">
          <div className="word-track">
            {/* We repeat the first word at the end for a seamless infinite loop */}
            <span className="word highlight-build">build</span>
            <span className="word highlight-ship">ship</span>
            <span className="word highlight-build">build</span>
          </div>
        </div>

        <span className="static-text">things.</span>
      </div>
    </div>
  );
};

export default BuilderStatement;