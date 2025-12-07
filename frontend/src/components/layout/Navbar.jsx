import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Menu, X } from 'lucide-react'; // Icons for the toggle
import LiveCounter from '../ui/LiveCounter';
import './Navbar.css';

const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false);

  // Close menu when a link is clicked
  const closeMenu = () => setIsOpen(false);

  return (
    <nav className="navbar">
      <div className="nav-container">
        <Link to="/" className="nav-logo" onClick={closeMenu}>
          C.C.Govardhan<span className="dot">.</span>
        </Link>

        {/* Right Side Wrapper */}
        <div className="nav-right">
            {/* Live Counter (Always Visible) */}
            <LiveCounter />

            {/* Mobile Toggle Button */}
            <button 
                className="mobile-menu-btn" 
                onClick={() => setIsOpen(!isOpen)}
                aria-label="Toggle Menu"
            >
                {isOpen ? <X size={24} /> : <Menu size={24} />}
            </button>

            {/* Links (Desktop + Mobile Dropdown) */}
            <div className={`nav-links ${isOpen ? 'open' : ''}`}>
                <Link to="/projects" onClick={closeMenu}>Projects</Link>
                <Link to="/blog" onClick={closeMenu}>Blog</Link>
                <Link to="/contact" onClick={closeMenu}>Contact</Link>
                <Link to="/admin" className="secret-btn" onClick={closeMenu}>Login</Link>
            </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;