import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { isAuthenticated } from '../../services/authService';

const ProtectedRoute = () => {
  if (!isAuthenticated()) {
    // If not logged in, kick to login page
    return <Navigate to="/admin" replace />;
  }

  // If logged in, show the child route (Dashboard)
  return <Outlet />;
};

export default ProtectedRoute;