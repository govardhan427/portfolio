import React, { useEffect, useState } from 'react';
import { X, Github, ExternalLink, Calendar, Layers, ChevronLeft, ChevronRight } from 'lucide-react';
import './ProjectModal.css';

const getIconUrl = (name) => {
  let cleanName = name.toLowerCase().replace(/\./g, '').replace(/\s/g, '');
  const mappings = { 'c++': 'cplusplus', 'c#': 'csharp', 'html': 'html5', 'css': 'css3', 'aws': 'amazonwebservices', 'js': 'javascript', 'postman': 'postman', 'node': 'nodejs', 'postgres': 'postgresql', 'drf': 'django' };
  if (mappings[cleanName]) cleanName = mappings[cleanName];
  return `https://cdn.jsdelivr.net/gh/devicons/devicon/icons/${cleanName}/${cleanName}-original.svg`;
};

const ProjectModal = ({ project, onClose }) => {
  const [imgIndex, setImgIndex] = useState(0);

  if (!project) return null;

  const images = project.images || [];
  const hasMultiple = images.length > 1;

  // Handle Keypress (Esc to close, Arrows to swipe)
  useEffect(() => {
    const handleKeyDown = (e) => { 
        if (e.key === 'Escape') onClose(); 
        if (e.key === 'ArrowRight' && hasMultiple) nextImage();
        if (e.key === 'ArrowLeft' && hasMultiple) prevImage();
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [onClose, hasMultiple]);

  const handleContentClick = (e) => e.stopPropagation();

  // Swipe Functions
  const nextImage = (e) => {
      if(e) e.stopPropagation();
      setImgIndex((prev) => (prev + 1) % images.length);
  };

  const prevImage = (e) => {
      if(e) e.stopPropagation();
      setImgIndex((prev) => (prev - 1 + images.length) % images.length);
  };

  const currentImage = images.length > 0 ? images[imgIndex].image : null;

  return (
    <div className="modal-overlay animate-fade-in" onClick={onClose}>
      <div className="modal-content animate-modal-entry" onClick={handleContentClick}>
        <button className="modal-close" onClick={onClose}><X size={24} /></button>

        {/* 1. Header Gallery */}
        <div className="modal-image-wrapper">
          {currentImage ? (
            <img src={currentImage} alt={project.title} className="modal-cover" />
          ) : (
            <div className="modal-placeholder"></div>
          )}

          {/* Navigation Arrows */}
          {hasMultiple && (
            <>
                <button className="gallery-btn prev" onClick={prevImage}><ChevronLeft size={24}/></button>
                <button className="gallery-btn next" onClick={nextImage}><ChevronRight size={24}/></button>
                <div className="gallery-counter">{imgIndex + 1} / {images.length}</div>
            </>
          )}

          <div className="modal-links">
            {project.github_link && (
              <a href={project.github_link} target="_blank" rel="noreferrer" className="modal-btn secondary">
                <Github size={18} /> Source
              </a>
            )}
            {project.demo_link && (
              <a href={project.demo_link} target="_blank" rel="noreferrer" className="modal-btn primary">
                <ExternalLink size={18} /> Live Demo
              </a>
            )}
          </div>
        </div>

        {/* 2. Details */}
        <div className="modal-body">
          <div className="modal-header-row">
            <h2 className="modal-title">{project.title}</h2>
            <span className="modal-date">
                <Calendar size={14} /> {new Date(project.created_at).toLocaleDateString()}
            </span>
          </div>
          
          <p className="modal-tagline">{project.tagline}</p>
          <div className="modal-desc">{project.description}</div>
          <div className="modal-divider"></div>

          <div className="modal-stack-section">
            <h4><Layers size={16} /> Tech Stack</h4>
            <div className="modal-stack-grid">
              {project.skills.map(skill => (
                <div key={skill.id} className="mini-skill-badge">
                  <img src={getIconUrl(skill.name)} alt={skill.name} className="mini-skill-icon" />
                  <span>{skill.name}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProjectModal;