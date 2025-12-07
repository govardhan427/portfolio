import React, { useRef } from 'react';
import { Briefcase, GraduationCap, Trophy, Flag, ChevronRight, ChevronLeft, Code, Terminal, Server, Layers } from 'lucide-react';
import './JourneyTimeline.css';

const JourneyTimeline = ({ items }) => {
  const scrollRef = useRef(null);
  const scroll = (direction) => {
    if (scrollRef.current) {
      const { current } = scrollRef;
      const scrollAmount = 320;
      current.scrollBy({ left: direction === 'left' ? -scrollAmount : scrollAmount, behavior: 'smooth' });
    }
  };

  const getIcon = (title) => {
    const t = title.toLowerCase();
    if (t.includes('school') || t.includes('college')) return <GraduationCap size={20} />;
    if (t.includes('work') || t.includes('intern')) return <Briefcase size={20} />;
    if (t.includes('code') || t.includes('python')) return <Code size={20} />;
    if (t.includes('django') || t.includes('backend')) return <Terminal size={20} />;
    if (t.includes('devops') || t.includes('docker')) return <Server size={20} />;
    if (t.includes('full-stack')) return <Layers size={20} />;
    return <Flag size={20} />;
  };

  if (!items || items.length === 0) return null;

  return (
    <div className="journey-section animate-fade-in">
      <div className="journey-controls">
        <button className="scroll-btn" onClick={() => scroll('left')}><ChevronLeft size={24} /></button>
        <button className="scroll-btn" onClick={() => scroll('right')}><ChevronRight size={24} /></button>
      </div>

      <div className="journey-track" ref={scrollRef}>
        <div className="journey-line"></div>

        {items.map((item, index) => (
          <div 
            key={item.id} 
            className="journey-card-wrapper" 
            style={{ animationDelay: `${index * 0.1}s` }}
          >
            {/* The Node (Interactive) */}
            <div className="journey-dot">
                {getIcon(item.title)}
                <div className="particle-burst"></div> {/* <--- CSS Particles */}
            </div>

            <div className="journey-card">
              <span className="journey-date">{item.date_range}</span>
              <h3 className="journey-title">{item.title}</h3>
              <h4 className="journey-subtitle">{item.subtitle}</h4>
              <p className="journey-desc">{item.description}</p>
            </div>
          </div>
        ))}
        
        <div style={{ minWidth: '50px' }}></div>
      </div>
    </div>
  );
};

export default JourneyTimeline;