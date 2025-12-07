import React, { useState, useEffect } from 'react';
import { ExternalLink, Github } from 'lucide-react';
import './ProjectCard.css';

const ProjectCard = ({ project, onClick }) => {
  const [currentImgIndex, setCurrentImgIndex] = useState(0);
  const [isHovered, setIsHovered] = useState(false);

  // Auto-Swipe Logic
  useEffect(() => {
    // Uses nested images for auto-swipe
    if (project.images && project.images.length > 1 && !isHovered) {
      const interval = setInterval(() => {
        setCurrentImgIndex((prev) => (prev + 1) % project.images.length);
      }, 3000);
      return () => clearInterval(interval);
    }
  }, [project.images, isHovered]);

  // CRITICAL FIX: Determine the URL source
  const currentImage = 
    (project.images && project.images.length > 0)
      ? project.images[currentImgIndex].image_url
      : project.featured_image_url
        ? project.featured_image_url 
        : 'https://images.unsplash.com/photo-1555066931-4365d14bab8c?auto=format&fit=crop&w=800&q=80';

  return (
    <div 
      className="project-card animate-fade-in" 
      onClick={() => onClick(project)}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <div className="card-image-wrapper">
        <img 
          // FIX 3: Use the correctly determined currentImage URL
          src={currentImage} 
          alt={project.title} 
          className="card-image transition-opacity" 
        />
        
        {/* Overlay only shows "View Details" on hover now */}
        <div className="card-overlay">
          <span className="view-details-btn">View Details</span>
        </div>

        {/* Slide Indicators */}
        {project.images && project.images.length > 1 && (
          <div className="card-dots">
            {project.images.map((_, idx) => (
              <span key={idx} className={`dot ${idx === currentImgIndex ? 'active' : ''}`}></span>
            ))}
          </div>
        )}
      </div>

      <div className="card-content">
        <div className="card-header">
          <h3 className="card-title">{project.title}</h3>
          <span className="project-badge">{project.featured ? 'Featured' : 'Dev'}</span>
        </div>
        
        <p className="card-desc">{project.tagline}</p>
        
        {/* Footer Area: Tags + Live Button */}
        <div className="card-footer">
          <div className="card-tags">
            {project.skills.slice(0, 2).map(skill => (
              <span key={skill.id} className="tech-tag">{skill.name}</span>
            ))}
          </div>

          {/* 🚨 MOVED HERE: Always Visible Live Button */}
          {project.demo_link && (
            <a 
              href={project.demo_link} 
              target="_blank" 
              rel="noreferrer" 
              className="live-demo-btn"
              onClick={(e) => e.stopPropagation()} 
              title="Open Live Site"
            >
              Live Demo <ExternalLink size={14} />
            </a>
          )}
        </div>
      </div>
      <div className="neon-border"></div>
    </div>
  );
};

export default ProjectCard;