import React from 'react';
import './ProjectFilters.css';

const ProjectFilters = ({ activeFilter, setActiveFilter }) => {
  const filters = [
    { id: 'ALL', label: 'All Work' },
    { id: 'WEB', label: 'Web / Full-Stack' },
    { id: 'DEVOPS', label: 'DevOps / Cloud' },
    { id: 'TOOLS', label: 'Scripts & Tools' },
  ];

  return (
    <div className="filter-container animate-fade-in">
      {filters.map((f) => (
        <button
          key={f.id}
          className={`filter-btn ${activeFilter === f.id ? 'active' : ''}`}
          onClick={() => setActiveFilter(f.id)}
        >
          {f.label}
        </button>
      ))}
    </div>
  );
};

export default ProjectFilters;