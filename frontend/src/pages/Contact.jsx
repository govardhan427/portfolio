import React, { useState } from 'react';
import { Mail, MapPin, Send, Linkedin, Github, Instagram } from 'lucide-react';
import { sendContactMessage } from '../services/portfolioService'; // <--- Import service
import './Contact.css';

const Contact = () => {
  const [formData, setFormData] = useState({ name: '', email: '', message: '' });
  const [status, setStatus] = useState(''); // 'sending', 'success', 'error'

  const handleSubmit = async (e) => {
    e.preventDefault();
    setStatus('sending');

    try {
        await sendContactMessage(formData);
        setStatus('success');
        setFormData({ name: '', email: '', message: '' }); // Clear form
        
        // Reset status after 3 seconds
        setTimeout(() => setStatus(''), 5000);
    } catch (error) {
        console.error("Contact Error:", error);
        setStatus('error');
    }
  };

  return (
    <div className="page-contact">
      <div className="contact-grid">
        {/* Left: Info */}
        <div className="contact-info animate-fade-in">
          <h1 className="contact-title">Let's Build <br/>Something <span className="highlight">Great.</span></h1>
          <p className="contact-desc">
            I'm currently available for freelance work and full-time engineering roles.
          </p>
          <div className="info-items">
            <div className="info-item">
                <div className="icon-box"><Mail size={20}/></div>
                <span>ccgovardhan60@gmail.com</span>
            </div>
            <div className="info-item">
                <div className="icon-box"><MapPin size={20}/></div>
                <span>kadapa,Andhrapradesh,India</span>
            </div>
          </div>

          <div className="social-links-big">
            <a href="https://github.com/govardhan427"><Github size={24}/></a>
            <a href="https://linkedin.com/in/govardhan427"><Linkedin size={24}/></a>
            <a href="https://instagram.com/govardhan_427"><Instagram size={20} /></a>
          </div>
        </div>

        {/* Right: Form */}
        <form className="contact-form animate-fade-in" onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Name</label>
            <input 
                type="text" 
                value={formData.name}
                onChange={(e) => setFormData({...formData, name: e.target.value})}
                required 
            />
          </div>
          <div className="form-group">
            <label>Email</label>
            <input 
                type="email" 
                value={formData.email}
                onChange={(e) => setFormData({...formData, email: e.target.value})}
                required 
            />
          </div>
          <div className="form-group">
            <label>Message</label>
            <textarea 
                rows="5"
                value={formData.message}
                onChange={(e) => setFormData({...formData, message: e.target.value})}
                required 
            ></textarea>
          </div>

          <button type="submit" className={`send-btn ${status}`} disabled={status === 'sending' || status === 'success'}>
            {status === 'sending' && 'Transmitting...'}
            {status === 'success' && 'Message Received!'}
            {status === 'error' && 'Failed. Try Again.'}
            {status === '' && <>Send Message <Send size={16} /></>}
          </button>
        </form>
      </div>
    </div>
  );
};

export default Contact;