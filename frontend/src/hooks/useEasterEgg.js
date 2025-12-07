import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

const useEasterEgg = () => {
  const [input, setInput] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const handleKeyDown = (e) => {
      // Append char and keep last 10 chars
      setInput((prev) => (prev + e.key).slice(-10));
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  useEffect(() => {
    // 1. "kappa" -> Go to Admin
    if (input.includes('kappa')) {
        navigate('/admin');
        setInput('');
    }
    
    // 2. "devmode" -> Toggle a class on body (Matrix Mode)
    if (input.includes('devmode')) {
        document.body.classList.toggle('dev-mode');
        alert("⚠️ DEVELOPER MODE ACTIVATED ⚠️");
        setInput('');
    }
  }, [input, navigate]);
};

export default useEasterEgg;