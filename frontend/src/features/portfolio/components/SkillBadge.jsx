import React, { useState } from 'react';
import { Layers } from 'lucide-react'; // Fallback icon
import './SkillBadge.css';

const SkillBadge = ({ skill }) => {
  const [imgError, setImgError] = useState(false);

  // Helper: Convert skill name to DevIcon URL
  const getIconUrl = (name) => {
    // 1. Clean the name (lowercase, remove spaces/dots)
    let cleanName = name.toLowerCase().replace(/\./g, '').replace(/\s/g, '');

    // 2. Manual Mappings for tricky names
    const mappings = {
      'c++': 'cplusplus',
      'c#': 'csharp',
      'html': 'html5',
      'css': 'css3',
      'aws': 'amazonwebservices',
      'js': 'javascript',
      'postman': 'postman',
      'node': 'nodejs',
      'postgres': 'postgresql',
      'postgresql': 'postgresql',
      'drf': 'django', // Re-use Django icon for DRF
      'restapi': 'fastapi' // Use generic or approximate
    };

    if (mappings[cleanName]) cleanName = mappings[cleanName];

    // 3. Return the CDN URL
    return `https://cdn.jsdelivr.net/gh/devicons/devicon/icons/${cleanName}/${cleanName}-original.svg`;
  };

  return (
    <div className="skill-badge animate-fade-in">
      <div className="skill-content">
        {/* Logo Section */}
        <div className="skill-icon">
            {!imgError ? (
                <img 
                    src={getIconUrl(skill.name)} 
                    alt={skill.name} 
                    onError={() => setImgError(true)} 
                />
            ) : (
                <Layers size={24} color="var(--text-muted)" /> // Fallback if no logo found
            )}
        </div>

        {/* Text Section */}
        <div className="skill-info">
            <span className="skill-name">{skill.name}</span>
            <div className="skill-bar-bg">
                <div 
                    className="skill-bar-fill" 
                    style={{ width: `${skill.proficiency}%` }}
                ></div>
            </div>
        </div>
      </div>
    </div>
  );
};

export default SkillBadge;