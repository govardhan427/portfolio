import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import PublicLayout from './components/layout/PublicLayout';
import ProtectedRoute from './components/layout/ProtectedRoute'; // Import Guard
import Home from './pages/Home';
import Login from './pages/Login';
import AdminDashboard from './pages/AdminDashboard';
import './styles/globals.css';
import Projects from './pages/Projects';
import BlogList from './pages/BlogList';
import BlogDetail from './pages/BlogDetail';
import Certifications from './pages/Certifications';
import Contact from './pages/Contact';
import NotFound from './pages/NotFound';
import Achievements from './pages/Achievements';
import Status from './pages/Status'; // Import

function App() {
  return (
    <Router>
      <Routes>
        {/* PUBLIC ROUTES (Visitors) */}
        <Route element={<PublicLayout />}>
          <Route path="/" element={<Home />} />
          <Route path="/projects" element={<Projects />} />
          <Route path="/certifications" element={<Certifications />} /> {/* <--- ADD THIS */}
          <Route path="/blog" element={<BlogList />} />
          <Route path="/blog/:slug" element={<BlogDetail />} />
          <Route path="/contact" element={<Contact />} />
          <Route path="/achievements" element={<Achievements />} />
        </Route>

        {/* AUTH ROUTE */}
        <Route path="/admin" element={<Login />} />

        {/* PROTECTED ADMIN ROUTES (The Spy Hub) */}
        <Route element={<ProtectedRoute />}>
           {/* We will create this Dashboard page in the next step */}
           <Route path="/admin/dashboard" element={<AdminDashboard />} />
           <Route path="/admin/dashboard" element={<div style={{color: 'white', padding: 100}}>Welcome Commander. <br/> Dashboard Loading...</div>} />
        </Route>

        {/* 404 */}
        <Route path="/status" element={<Status />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </Router>
  );
}

export default App;