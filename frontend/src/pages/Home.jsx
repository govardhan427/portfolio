import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { 
  ArrowRight, Github, Linkedin, Mail, Instagram, 
  FileText, Award, Zap, Activity, 
  Trophy, Star, Code, GitBranch, Medal, 
  ExternalLink, Image as ImageIcon // <--- Used for Cert Image Button
} from 'lucide-react';
import HeroSection from '../features/portfolio/components/HeroSection';
import ProjectCard from '../features/portfolio/components/ProjectCard';
import SkillBadge from '../features/portfolio/components/SkillBadge';
import JourneyTimeline from '../features/portfolio/components/JourneyTimeline';
import BuilderStatement from '../features/portfolio/components/BuilderStatement';
import ProjectModal from '../features/portfolio/components/ProjectModal'; // <--- Import Modal
import { getHomeData } from '../services/portfolioService';
import api from '../services/api';
import '../styles/HomeLayout.css';
import './Achievements.css';

const Home = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [latency, setLatency] = useState(null);
  const [selectedProject, setSelectedProject] = useState(null); // <--- State for Modal

  useEffect(() => {
    const initData = async () => {
      try {
        // 1. Fetch Main Content
        const homeData = await getHomeData();
        setData(homeData);

        // 2. Fetch API Latency
        const statusRes = await api.get('/features/status/');
        setLatency(statusRes.data.latency);
      } catch (error) {
        console.error("Failed to load system data", error);
      } finally {
        setLoading(false);
      }
    };
    initData();
  }, []);

  const getBadgeIcon = (name) => {
    const icons = {
      Trophy: <Trophy size={32} />, Star: <Star size={32} />, 
      Code: <Code size={32} />, Zap: <Zap size={32} />, 
      GitBranch: <GitBranch size={32} />, Award: <Award size={32} />, 
      Medal: <Medal size={32} />
    };
    return icons[name] || <Trophy size={32} />;
  };

  if (loading) {
    return (
      <div style={{ height: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <h2 style={{ color: 'var(--neon-cyan)', fontFamily: 'monospace' }}>Initializing System...</h2>
      </div>
    );
  }

  return (
    <div className="page-home">
      {/* 1. Hero Section */}
      <HeroSection 
        title={data?.hero_title} 
        subtitle={data?.about_text} 
      />

      {/* 1.5 Builder Statement */}
      <BuilderStatement />

      {/* 2. Featured Projects Section */}
      <section className="section-container">
        <div className="section-header">
          <h2 className="section-title">Featured <span style={{color: 'var(--neon-cyan)'}}>Work</span></h2>
          <div className="section-line"></div>
          <Link to="/projects" className="section-link">View All <ArrowRight size={14}/></Link>
        </div>

        {data?.featured_projects && data.featured_projects.length > 0 ? (
            <div className="projects-grid">
                {data.featured_projects.map((project) => (
                    <ProjectCard 
                        key={project.id} 
                        project={project} 
                        onClick={setSelectedProject} // <--- Open Modal on Click
                    />
                ))}
            </div>
        ) : (
            <div className="empty-state">
                No Featured Projects Found. <br/> 
                <small>Go to Admin Panel - Projects</small>
            </div>
        )}
      </section>

      {/* 3. Skills Overview Section */}
      <section className="section-container">
        <div className="section-header">
          <h2 className="section-title">Technical <span style={{color: 'var(--neon-purple)'}}>Arsenal</span></h2>
          <div className="section-line"></div>
          <Link to="/skills" className="section-link">Full Stack <ArrowRight size={14}/></Link>
        </div>

        {data?.skills && data.skills.length > 0 ? (
            <div className="skills-grid">
                {data.skills.map((s) => (
                    <SkillBadge key={s.id} skill={s} />
                ))}
            </div>
        ) : (
            <div className="empty-state">
                No Skills Found. <br/>
                <small>Go to Admin Panel - Skills</small>
            </div>
        )}
      </section>

      {/* 4. Journey Timeline */}
      {data?.journey && data.journey.length > 0 && (
        <section className="section-container">
          <div className="section-header">
            <h2 className="section-title">My <span style={{color: 'var(--neon-cyan)'}}>Journey</span></h2>
            <div className="section-line"></div>
          </div>
          <JourneyTimeline items={data.journey} />
        </section>
      )}

      {/* 5. Certifications Section */}
      <section className="section-container">
        <div className="section-header">
            <h2 className="section-title">Credentials & <span style={{color: 'var(--neon-green)'}}>Certs</span></h2>
            <div className="section-line"></div>
        </div>

        {data?.certificates && data.certificates.length > 0 ? (
            <div className="certs-grid">
                {data.certificates.map((cert) => (
                    <div key={cert.id} className="cert-card animate-fade-in">
                        <div className="cert-icon"><Award size={24} color="var(--neon-green)" /></div>
                        <div className="cert-info">
                            <h3>{cert.name}</h3>
                            <p>{cert.issuer} • {new Date(cert.date_issued).getFullYear()}</p>
                        </div>
                        
                        <div className="cert-actions-row">
                            {cert.credential_url && (
                                <a href={cert.credential_url} target="_blank" rel="noreferrer" className="cert-btn-small">
                                    Verify <ExternalLink size={12} />
                                </a>
                            )}
                            {cert.image && (
                                <a href={cert.image_url} target="_blank" rel="noreferrer" className="cert-btn-small image">
                                    View <ImageIcon size={12} />
                                </a>
                            )}
                        </div>
                    </div>
                ))}
            </div>
        ) : (
            <div className="empty-state">
                No Certificates Found. <br/>
                <small>Go to Admin Panel - Certifications</small>
            </div>
        )}
      </section>

      {/* 6. Achievements / Badges Section */}
      {data?.achievements && data.achievements.length > 0 && (
        <section className="section-container">
            <div className="section-header">
                <h2 className="section-title">Unlocked <span style={{color: '#ffd700'}}>Badges</span></h2>
                <div className="section-line"></div>
            </div>
            <div className="badges-grid">
                {data.achievements.map((item) => (
                    <div key={item.id} className="badge-card animate-fade-in">
                        <div className="badge-glow"></div>
                        <div className="badge-icon-wrapper">{getBadgeIcon(item.icon_name)}</div>
                        <div className="badge-content">
                            <h3 className="badge-title">{item.title}</h3>
                            <p className="badge-desc">{item.description}</p>
                        </div>
                    </div>
                ))}
            </div>
        </section>
      )}

      {/* 7. Engineering Blog Teaser */}
      <section className="section-container highlight-section">
        <div className="highlight-content">
            <FileText size={40} color="var(--neon-cyan)" />
            <div>
                <h3>Engineering Logs</h3>
                <p>Read my thoughts on System Design, DevOps, and Full-Stack patterns.</p>
            </div>
            <Link to="/blog" className="btn-glow">Read Articles</Link>
        </div>
      </section>

      {/* 8. Contact CTA */}
      <section className="cta-section">
         <h2 className="cta-title">Ready to build something <span style={{color: 'var(--neon-green)'}}>extraordinary?</span></h2>
         <p className="cta-subtitle">I'm currently available for freelance projects and full-time roles.</p>
         <Link to="/contact" className="btn-primary-large">
            <Zap size={20} /> Let's Talk
         </Link>
      </section>

      {/* 9. Footer */}
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

      {/* 10. Project Modal (Rendered conditionally) */}
      {selectedProject && (
        <ProjectModal 
            project={selectedProject} 
            onClose={() => setSelectedProject(null)} 
        />
      )}
    </div>
  );
};

export default Home;