import React, { useEffect, useState } from 'react';
import { getDashboardStats, getRecentVisitors } from '../services/adminService';
import { logout } from '../services/authService';
import { Activity, Users, Eye, LogOut, Monitor } from 'lucide-react';
import './AdminDashboard.css';
import FileManager from '../features/vault/components/FileManager';
import VisitorMap from '../features/admin/components/VisitorMap';

const AdminDashboard = () => {
  const [stats, setStats] = useState(null);
  const [visitors, setVisitors] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadData = async () => {
      try {
        const [statsData, visitorsData] = await Promise.all([
            getDashboardStats(),
            getRecentVisitors()
        ]);
        setStats(statsData);
        
        // 🚨 FIX: Handle the raw list from Django properly
        const validVisitors = Array.isArray(visitorsData) ? visitorsData : (visitorsData.results || []);
        
        setVisitors(validVisitors); 
      } catch (error) {
        console.error("Dashboard Error", error);
      } finally {
        setLoading(false);
      }
    };
    loadData();
  }, []);

  if (loading) return <div className="dashboard-loading">Accessing Mainframe...</div>;

  return (
    <div className="dashboard-container">
      {/* 1. Header */}
      <header className="dashboard-header">
        <div className="header-logo">
          <span className="status-dot"></span>
          <h2>SYSTEM COMMAND</h2>
        </div>
        <button onClick={logout} className="logout-btn">
          <LogOut size={16} /> Disconnect
        </button>
      </header>

      <div className="dashboard-content">
        
        {/* 2. Top Stats Row (Full Width) */}
        <div className="stats-grid">
          <div className="stat-card">
            <div className="stat-icon"><Users color="#39ff14" /></div>
            <div className="stat-info">
              <h3>Total Visitors</h3>
              <p className="stat-value">{stats?.overview?.total_visitors}</p>
            </div>
          </div>
          
          <div className="stat-card">
            <div className="stat-icon"><Activity color="#00f3ff" /></div>
            <div className="stat-info">
              <h3>Active Today</h3>
              <p className="stat-value">{stats?.overview?.active_today}</p>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon"><Eye color="#bc13fe" /></div>
            <div className="stat-info">
              <h3>Total Pageviews</h3>
              <p className="stat-value">{stats?.overview?.total_pageviews}</p>
            </div>
          </div>
        </div>

        {/* 3. Main Split: Map (Left) vs Logs/Charts (Right) */}
        <div className="main-split-layout">
            
            {/* LEFT COLUMN: Map */}
            <div className="left-column">
                <div className="panel map-panel-vertical">
                    <h3>Global Surveillance</h3>
                    <VisitorMap visitors={visitors} />
                </div>
            </div>

            {/* RIGHT COLUMN: Logs & Files */}
            <div className="right-column">
                
                {/* Live Logs */}
                <div className="panel visitors-panel">
                    <h3>Live Traffic Stream</h3>
                    <div className="visitor-table-wrapper">
                        <table className="visitor-table">
                            <thead>
                                <tr>
                                    <th>IP Address</th>
                                    <th>Device</th>
                                    <th>Time</th>
                                </tr>
                            </thead>
                            <tbody>
                                {visitors.slice(0, 5).map((v) => (
                                    <tr key={v.id}>
                                        <td className="mono">{v.ip_address}</td>
                                        <td><Monitor size={12} /> {v.device_type || 'Unknown'}</td>
                                        <td>{new Date(v.last_visit).toLocaleTimeString()}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>

                {/* Top Pages */}
                <div className="panel top-pages-panel">
                    <h3>Most Accessed Nodes</h3>
                    <div className="bar-chart-container">
                        {stats?.top_pages.slice(0, 3).map((page, index) => (
                            <div key={index} className="bar-row">
                                <span className="bar-label">{page.path}</span>
                                <div className="bar-track">
                                    <div 
                                        className="bar-fill" 
                                        style={{ width: `${(page.views / stats.overview.total_pageviews) * 100}%` }}
                                    ></div>
                                </div>
                                <span className="bar-count">{page.views}</span>
                            </div>
                        ))}
                    </div>
                </div>

                {/* File Vault */}
                <FileManager />
                
            </div>
        </div>

      </div>
    </div>
  );
};

export default AdminDashboard;