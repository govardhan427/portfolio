import React, { useState, useRef, useEffect } from 'react';
import { MessageSquare, X, Send, Bot, Sparkles } from 'lucide-react';
import { sendChatQuery } from '../../../services/portfolioService';
import { Link } from 'react-router-dom';
import './AIChatBot.css';

const AIChatBot = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [showLabel, setShowLabel] = useState(true); // Starts open
  
  const [messages, setMessages] = useState([
    { id: 1, text: "Hello! I am Govardhan's AI Assistant. Ask me about his projects, skills, or experience.", sender: 'bot' }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  // 🔄 LOOP LOGIC: Toggle the label every 5 seconds
  useEffect(() => {
    const interval = setInterval(() => {
        setShowLabel((prev) => !prev);
    }, 7000); // 5 Seconds Open, 5 Seconds Closed

    return () => clearInterval(interval);
  }, []);

  // Auto-scroll logic
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isOpen]);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMsg = { id: Date.now(), text: input, sender: 'user' };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    const response = await sendChatQuery(userMsg.text);
    
    const botMsg = { 
        id: Date.now() + 1, 
        text: response.text, 
        sender: 'bot',
        link: response.related_link 
    };
    setMessages(prev => [...prev, botMsg]);
    setLoading(false);
  };

  return (
    <div className="chatbot-container">
      {/* 2. The Shape-Shifting Button */}
      {!isOpen && (
        <button 
            className={`chat-toggle-btn ${showLabel ? 'expanded' : ''} animate-float`} 
            onClick={() => setIsOpen(true)}
            // Optional: Keep it open if user hovers
            onMouseEnter={() => setShowLabel(true)}
        >
          {/* Cool Bot Icon */}
          <div className="icon-wrapper">
             <Bot size={24} />
             <span className="online-indicator"></span>
          </div>
          {/* The Text that appears/disappears */}
          <span className="chat-btn-label">Hey! Chat with me?</span>
        </button>
      )}

      {/* Chat Window */}
      {isOpen && (
        <div className="chat-window animate-fade-in-up">
          <div className="chat-header">
            <div className="header-info">
                <Sparkles size={18} color="var(--neon-green)" />
                <span>Govardhan AI</span>
            </div>
            <button onClick={() => setIsOpen(false)} className="close-btn"><X size={18} /></button>
          </div>

          <div className="chat-messages">
            {messages.map((msg) => (
              <div key={msg.id} className={`message ${msg.sender}`}>
                <p>{msg.text}</p>
                {msg.link && (
                    <Link to={msg.link} className="chat-link-btn" onClick={() => setIsOpen(false)}>
                        View Details →
                    </Link>
                )}
              </div>
            ))}
            {loading && <div className="message bot typing">Processing...</div>}
            <div ref={messagesEndRef} />
          </div>

          <form className="chat-input-area" onSubmit={handleSend}>
            <input 
                type="text" 
                placeholder="Ask something..." 
                value={input}
                onChange={(e) => setInput(e.target.value)}
                disabled={loading}
            />
            <button type="submit" disabled={loading || !input.trim()}>
                <Send size={16} />
            </button>
          </form>
        </div>
      )}
    </div>
  );
};

export default AIChatBot;