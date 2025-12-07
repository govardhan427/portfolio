import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Search, Github, Linkedin, Mail, Instagram, Activity } from 'lucide-react'; // <--- Added Icons
import ProjectCard from '../features/portfolio/components/ProjectCard';
import ProjectFilters from '../features/portfolio/components/ProjectFilters';
import ProjectModal from '../features/portfolio/components/ProjectModal';
import { getProjects } from '../services/portfolioService';
import api from '../services/api'; // <--- Import API for latency check
import './Projects.css';
import '../styles/HomeLayout.css'; // Ensure footer styles work

const Projects = () => {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeFilter, setActiveFilter] = useState('ALL');
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedProject, setSelectedProject] = useState(null);
  const [latency, setLatency] = useState(null); // <--- Latency State

  useEffect(() => {
    const initData = async () => {
      try {
        const [projectData, statusRes] = await Promise.all([
            getProjects(),
            api.get('/features/status/')
        ]);
        setProjects(projectData);
        setLatency(statusRes.data.latency);
      } catch (error) {
        console.error("Error loading data", error);
      } finally {
        setLoading(false);
      }
    };
    initData();
  }, []);

  // 🔍 THE FILTERING LOGIC
  const filteredProjects = projects.filter((project) => {
    const matchesSearch = project.title.toLowerCase().includes(searchQuery.toLowerCase()) || 
                          project.tagline.toLowerCase().includes(searchQuery.toLowerCase());

    let matchesCategory = true;
    if (activeFilter !== 'ALL') {
        const skillNames = project.skills.map(s => s.name.toUpperCase());
        const skillCategories = project.skills.map(s => s.category); 

        if (activeFilter === 'DEVOPS') {
            matchesCategory = skillCategories.includes('DEVOPS') || 
                              skillNames.some(n => ['DOCKER', 'KUBERNETES', 'AWS', 'LINUX', 'JENKINS'].includes(n));
        } else if (activeFilter === 'WEB') {
            matchesCategory = skillCategories.includes('FRONT') || skillCategories.includes('BACK') ||
                              skillNames.some(n => ['REACT', 'DJANGO', 'PYTHON', 'JS'].includes(n));
        } else if (activeFilter === 'TOOLS') {
            matchesCategory = skillCategories.includes('TOOL');
        }
    }
    return matchesSearch && matchesCategory;
  });

  return (
    <div className="page-projects">
      <div className="projects-header">
        <h1 className="page-title">My <span className="highlight">Work</span></h1>
        <p className="page-subtitle">A collection of systems, deployments, and experiments.</p>
        
        {/* Search Bar */}
        <div className="search-bar-wrapper">
            <Search className="search-icon" size={20} />
            <input 
                type="text" 
                placeholder="Search projects (e.g. 'Django', 'API')..." 
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
            />
        </div>
      </div>

      {/* Filter Buttons */}
      <ProjectFilters activeFilter={activeFilter} setActiveFilter={setActiveFilter} />

      {/* Grid */}
      {loading ? (
        <div className="loading-state">Loading Archives...</div>
      ) : (
        <div className="projects-grid-full">
            {filteredProjects.length > 0 ? (
                filteredProjects.map(project => (
                    <ProjectCard 
                        key={project.id} 
                        project={project} 
                        onClick={setSelectedProject} 
                    />
                ))
            ) : (
                <div className="no-results">
                    No projects found matching these criteria.
                </div>
            )}
        </div>
      )}

      {/* Project Modal */}
      {selectedProject && (
        <ProjectModal 
            project={selectedProject} 
            onClose={() => setSelectedProject(null)} 
        />
      )}

      {/* Footer (Matches Home Page) */}
      <footer className="home-footer">
        <div className="footer-content">
            <div className="footer-logo">C.C.Govardhan<span style={{color: 'var(--neon-cyan)'}}>.</span></div>
            
            <div className="footer-links">
                <a href="https://github.com/govardhan427" target="_blank" rel="noreferrer"><Github size={20} /></a>
                <a href="https://linkedin.com/in/govardhan427" target="_blank" rel="noreferrer"><Linkedin size={20} /></a>
                <a href="https://instagram.com/govardhan_427" target="_blank" rel="noreferrer"><Instagram size={20} /></a>
                <Link to="/contact"><Mail size={20} /></Link>
            </div>

            <div className="footer-status">
                <Link to="/status" className="status-link">
                    <span className="status-dot"></span> System Status
                </Link>
                {latency && (
                    <span className="latency-badge">
                        <Activity size={12} /> {latency}
                    </span>
                )}
            </div>
        </div>
        <p className="footer-copyright">© 2025 Govardhan. Built with React, Django & DevOps.</p>
      </footer>
    </div>
  );
};

export default Projects;