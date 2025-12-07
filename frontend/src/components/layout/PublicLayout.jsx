import React from 'react';
import { Outlet } from 'react-router-dom';
import Navbar from './Navbar';
import useVisitorTracker from '../../features/analytics/hooks/useVisitorTracker';
import AIChatBot from '../../features/portfolio/components/AIChatBot';
import useEasterEgg from '../../hooks/useEasterEgg';

const PublicLayout = () => {
  // Activate Spy Mode 🕵️‍♂️
  useVisitorTracker();
  useEasterEgg();

  return (
    <div className="public-layout">
      <Navbar />
      <main className="content">
        {/* Outlet renders the current page (Home, Projects, etc.) */}
        <Outlet />
      </main>
      <AIChatBot />
    </div>
  );
};

export default PublicLayout;