import React, { useEffect, useRef, useState } from 'react';
import { ArrowRight, Download, Github, Linkedin, Mail,Instagram,Eye } from 'lucide-react';
import './HeroSection.css';


// ✨ Background Particles (Same as before)
const BackgroundParticles = () => {
  const particles = Array.from({ length: 20 }).map((_, i) => ({
    id: i,
    left: Math.random() * 100,
    top: Math.random() * 100,
    delay: Math.random() * 5,
    duration: 5 + Math.random() * 10
  }));

  return (
    <div className="particles-container">
      {particles.map((p) => (
        <div 
          key={p.id} 
          className="particle"
          style={{
            left: `${p.left}%`,
            top: `${p.top}%`,
            animationDelay: `${p.delay}s`,
            animationDuration: `${p.duration}s`
          }}
        />
      ))}
    </div>
  );
};

const HeroSection = ({ title, subtitle }) => {
  const cardRef = useRef(null);
  
  // 🔄 Icon Cycling Logic
  const icons = [
    { icon: "⚛️", color: "#61dafb", name: "React" },
    { icon: "🐍", color: "#39ff14", name: "Django" },
    { icon: "🐳", color: "#2496ed", name: "Docker" },
    { icon: "🚀", color: "#bc13fe", name: "DevOps" },
  ];
  
  const [currentIcon, setCurrentIcon] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentIcon((prev) => (prev + 1) % icons.length);
    }, 2500); // Change every 2.5 seconds
    return () => clearInterval(interval);
  }, []);

  // 3D Tilt Logic
  const handleMouseMove = (e) => {
    const card = cardRef.current;
    if (!card) return;
    const rect = card.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    const centerX = rect.width / 2;
    const centerY = rect.height / 2;
    const rotateX = ((y - centerY) / centerY) * -10;
    const rotateY = ((x - centerX) / centerX) * 10;
    card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
  };

  const handleMouseLeave = () => {
    if (cardRef.current) {
        cardRef.current.style.transform = `perspective(1000px) rotateX(0deg) rotateY(0deg)`;
    }
  };

  return (
    <section className="hero-container">
      <BackgroundParticles />

      {/* Left: Text Content */}
      <div className="hero-content">
        <div className="hero-badge animate-slide-up" style={{animationDelay: '0.1s'}}>
           Available for Hire
        </div>
        
        <h1 className="hero-title animate-slide-up" style={{animationDelay: '0.2s'}}>
          Hi, I'm Govardhan<span className="dot">.</span>
        </h1>
        
        <h2 className="hero-subtitle animate-slide-up" style={{animationDelay: '0.3s'}}>
          {title || "Full-Stack Developer & DevOps Engineer"}
        </h2>
        
        <p className="hero-desc animate-slide-up" style={{animationDelay: '0.4s'}}>
          {subtitle || "I build scalable web apps, automate deployments, and turn complex problems into clean code."}
        </p>
        
        <div className="hero-actions animate-slide-up" style={{animationDelay: '0.5s'}}>
          <a href="/projects" className="btn btn-primary">
            View Work <ArrowRight size={18} />
          </a>
          <a 
href="https://drive.google.com/file/d/1VsBckxKf0bokuL8CC6QaU2rx9qWA7SGA/view?usp=drive_link" 
              target="_blank" 
              rel="noopener noreferrer" 
              className="btn btn-outline"
              download // Optional: Hints browser to download instead of open
            >
              Resume <Eye size={18} />
            </a>
        </div>

        <div className="hero-socials animate-slide-up" style={{animationDelay: '0.6s'}}>
          <a href="https://github.com/govardhan427"><Github size={20} /></a>
          <a href="https://linkedin.com/in/govardhan427"><Linkedin size={20} /></a>
          <a href="/contact"><Mail size={20} /></a>
          <a href="https://instagram.com/govardhan_427" target="_blank" rel="noreferrer"><Instagram size={20} /></a>
        </div>
      </div>

      {/* Right: 3D Image Card */}
      <div 
        className="hero-image-wrapper animate-float"
        onMouseMove={handleMouseMove}
        onMouseLeave={handleMouseLeave}
        ref={cardRef}
      >
        <div className="hero-card-glow"></div>
        <div className="hero-image-card">
            <img 
              src="https://res.cloudinary.com/dqw1t0dul/image/upload/v1765019802/IMG_20251206_164007_msjll4.jpg" 
              alt="Govardhan" 
              className="profile-img animate-breathe" 
            />
            
            {/* ✨ THE NEW CYCLING ORB (Top Right) */}
            <div className="tech-orb-wrapper">
               <div 
                 key={currentIcon} /* Key change triggers animation re-render */
                 className="tech-orb animate-pop-in"
                 style={{ 
                    borderColor: icons[currentIcon].color,
                    boxShadow: `0 0 20px ${icons[currentIcon].color}40` // 40 = opacity
                 }}
               >
                  {icons[currentIcon].icon}
               </div>
            </div>

        </div>
      </div>
      
      <div className="bg-glow-blob top-right"></div>
      <div className="bg-glow-blob bottom-left"></div>
    </section>
  );
};

export default HeroSection;