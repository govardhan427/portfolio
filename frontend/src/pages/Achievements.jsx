import React, { useState, useEffect } from 'react';
import { getHomeData } from '../services/portfolioService';
import { Trophy, Star, Code, Zap, GitBranch, Award, Medal } from 'lucide-react';
import './Achievements.css';

// Icon Map helper
const getIcon = (name) => {
  const icons = {
    Trophy: <Trophy size={32} />,
    Star: <Star size={32} />,
    Code: <Code size={32} />,
    Zap: <Zap size={32} />,
    GitBranch: <GitBranch size={32} />,
    Award: <Award size={32} />,
    Medal: <Medal size={32} />
  };
  return icons[name] || <Trophy size={32} />;
};

const Achievements = () => {
  const [achievements, setAchievements] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getHomeData().then(data => {
        if (data?.achievements) setAchievements(data.achievements);
        setLoading(false);
    });
  }, []);

  if (loading) return <div className="loading-state">Loading Trophy Room...</div>;

  return (
    <div className="page-achievements">
      <div className="achievements-header">
        <h1 className="page-title">Unlocked <span className="highlight">Badges</span></h1>
        <p className="page-subtitle">Milestones, Hackathons, and Special Events.</p>
      </div>

      <div className="badges-grid">
        {achievements.length === 0 ? (
            <div className="empty-state">No badges unlocked yet.</div>
        ) : (
            achievements.map((item, index) => (
            <div key={item.id} className="badge-card animate-fade-in" style={{ animationDelay: `${index * 0.1}s` }}>
                <div className="badge-glow"></div>
                <div className="badge-icon-wrapper">
                    {getIcon(item.icon_name)}
                </div>
                <div className="badge-content">
                    <h3 className="badge-title">{item.title}</h3>
                    <p className="badge-desc">{item.description}</p>
                    <div className="badge-meta">
                        Unlocked: {new Date(item.date_earned).toLocaleDateString()}
                    </div>
                </div>
            </div>
            ))
        )}
      </div>
    </div>
  );
};

export default Achievements;