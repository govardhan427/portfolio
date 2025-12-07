import React, { useState, useEffect } from 'react';
import { getHomeData } from '../services/portfolioService';
import { Award, Calendar, ExternalLink, CheckCircle, Image as ImageIcon } from 'lucide-react';
import './Certifications.css';

const Certifications = () => {
  const [certs, setCerts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getHomeData().then(data => {
        if(data?.certificates) {
            setCerts(data.certificates);
        }
        setLoading(false);
    });
  }, []);

  if (loading) return <div className="loading-state">Loading Timeline...</div>;

  return (
    <div className="page-certs">
      <div className="certs-header">
        <h1 className="page-title">Career <span style={{color: 'var(--neon-green)'}}>Timeline</span></h1>
        <p className="page-subtitle">Milestones, Credentials, and Technical Achievements.</p>
      </div>

      <div className="timeline-container">
        {certs.length === 0 ? (
            <div className="empty-state">No certifications found. Add them in the Admin Panel.</div>
        ) : (
            certs.map((cert, index) => (
            <div key={cert.id} className={`timeline-item ${index % 2 === 0 ? 'left' : 'right'} animate-fade-in`}>
                
                {/* The Dot on the Central Line */}
                <div className="timeline-dot">
                    <Award size={20} color="black" />
                </div>

                {/* The Content Card */}
                <div className="timeline-content">
                    <div className="cert-date">
                        <Calendar size={14} /> 
                        {new Date(cert.date_issued).toLocaleDateString(undefined, { year: 'numeric', month: 'long' })}
                    </div>
                    
                    <h3 className="cert-title">{cert.name}</h3>
                    <p className="cert-issuer">Issued by {cert.issuer}</p>
                    
                    <div className="cert-tags">
                        <span className="mini-tag"><CheckCircle size={10}/> Verified</span>
                    </div>

                    {/* Action Buttons */}
                    <div className="cert-actions">
                        {cert.credential_url && (
                            <a href={cert.credential_url} target="_blank" rel="noreferrer" className="cert-verify-btn">
                                Verify Link <ExternalLink size={14} />
                            </a>
                        )}
                        
                        {/* CRITICAL FIX HERE */}
                        {cert.image_url && ( /* 1. Change from cert.image to cert.image_url */
                            <a href={cert.image_url} target="_blank" rel="noreferrer" className="cert-verify-btn image-btn"> 
                                {/* 2. Change link href from cert.image to cert.image_url */}
                                View Image <ImageIcon size={14} />
                            </a>
                        )}
                    </div>
                </div>
            </div>
            ))
        )}
      </div>
    </div>
  );
};
export default Certifications;