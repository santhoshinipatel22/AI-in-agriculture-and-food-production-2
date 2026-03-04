import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './AdminDashboard.css';

export default function AdminDashboard() {
  const [stats, setStats] = useState({
    totalFarmers: 0,
    activeCrops: 0,
    diseaseDetections: 0,
    iotDevices: 0,
    subsidiesApplied: 0,
  });
  const [tab, setTab] = useState('overview');
  const [loading, setLoading] = useState(true);

  const API_URL = process.env.REACT_APP_API_URL;
  const token = localStorage.getItem('accessToken');

  useEffect(() => {
    fetchAdminStats();
  }, []);

  const fetchAdminStats = async () => {
    try {
      const response = await axios.get(
        `${API_URL}/api/admin/stats`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      setStats(response.data.data);
    } catch (error) {
      console.error('Error fetching admin stats:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="admin-dashboard">
      <h1>Admin Dashboard</h1>
      <p>System Overview and Management</p>

      {loading ? (
        <div className="loading">Loading...</div>
      ) : (
        <>
          {/* Stats Cards */}
          <section className="stats-section">
            <div className="stat-card">
              <h3>Total Farmers</h3>
              <p className="stat-number">{stats.totalFarmers}</p>
              <p className="stat-description">Active users</p>
            </div>
            <div className="stat-card">
              <h3>Active Crops</h3>
              <p className="stat-number">{stats.activeCrops}</p>
              <p className="stat-description">Currently growing</p>
            </div>
            <div className="stat-card">
              <h3>Disease Detections</h3>
              <p className="stat-number">{stats.diseaseDetections}</p>
              <p className="stat-description">Total detected</p>
            </div>
            <div className="stat-card">
              <h3>IoT Devices</h3>
              <p className="stat-number">{stats.iotDevices}</p>
              <p className="stat-description">Connected sensors</p>
            </div>
            <div className="stat-card">
              <h3>Subsidy Applications</h3>
              <p className="stat-number">{stats.subsidiesApplied}</p>
              <p className="stat-description">Total applied</p>
            </div>
          </section>

          {/* Tabs */}
          <section className="admin-section">
            <div className="tab-navigation">
              <button
                className={`tab-btn ${tab === 'overview' ? 'active' : ''}`}
                onClick={() => setTab('overview')}
              >
                Overview
              </button>
              <button
                className={`tab-btn ${tab === 'farmers' ? 'active' : ''}`}
                onClick={() => setTab('farmers')}
              >
                Farmers
              </button>
              <button
                className={`tab-btn ${tab === 'models' ? 'active' : ''}`}
                onClick={() => setTab('models')}
              >
                AI Models
              </button>
              <button
                className={`tab-btn ${tab === 'subsidies' ? 'active' : ''}`}
                onClick={() => setTab('subsidies')}
              >
                Subsidies
              </button>
              <button
                className={`tab-btn ${tab === 'system' ? 'active' : ''}`}
                onClick={() => setTab('system')}
              >
                System
              </button>
            </div>

            {/* Tab Content */}
            {tab === 'overview' && (
              <div className="tab-content">
                <h2>System Overview</h2>
                <div className="info-grid">
                  <div className="info-card">
                    <h3>Platform Status</h3>
                    <p className="status-badge online">✓ Online</p>
                    <p>All systems operational</p>
                  </div>
                  <div className="info-card">
                    <h3>Database</h3>
                    <p className="status-badge online">✓ Connected</p>
                    <p>MongoDB - Healthy</p>
                  </div>
                  <div className="info-card">
                    <h3>API Server</h3>
                    <p className="status-badge online">✓ Running</p>
                    <p>Node.js - Port 5000</p>
                  </div>
                  <div className="info-card">
                    <h3>Cache Server</h3>
                    <p className="status-badge online">✓ Connected</p>
                    <p>Redis - Responsive</p>
                  </div>
                </div>
              </div>
            )}

            {tab === 'farmers' && (
              <div className="tab-content">
                <h2>Farmer Management</h2>
                <div className="management-actions">
                  <button className="btn btn-primary">View All Farmers</button>
                  <button className="btn btn-secondary">Filter by Region</button>
                  <button className="btn btn-secondary">View Reports</button>
                </div>
              </div>
            )}

            {tab === 'models' && (
              <div className="tab-content">
                <h2>AI Model Management</h2>
                <div className="models-grid">
                  <div className="model-card">
                    <h3>Disease Detection Model</h3>
                    <p>Accuracy: 94%</p>
                    <p>Version: 2.1.0</p>
                    <button>Update Model</button>
                  </div>
                  <div className="model-card">
                    <h3>Crop Recommendation</h3>
                    <p>Accuracy: 87%</p>
                    <p>Version: 1.8.0</p>
                    <button>Update Model</button>
                  </div>
                  <div className="model-card">
                    <h3>Price Prediction</h3>
                    <p>Accuracy: 82%</p>
                    <p>Version: 2.0.0</p>
                    <button>Update Model</button>
                  </div>
                  <div className="model-card">
                    <h3>Yield Forecasting</h3>
                    <p>Accuracy: 88%</p>
                    <p>Version: 1.9.0</p>
                    <button>Update Model</button>
                  </div>
                </div>
              </div>
            )}

            {tab === 'subsidies' && (
              <div className="tab-content">
                <h2>Government Subsidies</h2>
                <div className="subsidy-actions">
                  <button className="btn btn-primary">Add New Subsidy</button>
                  <button className="btn btn-secondary">Review Applications</button>
                  <button className="btn btn-secondary">Approve/Reject</button>
                </div>
              </div>
            )}

            {tab === 'system' && (
              <div className="tab-content">
                <h2>System Settings</h2>
                <div className="settings-grid">
                  <div className="setting-item">
                    <label>API Rate Limit (requests/sec)</label>
                    <input type="number" defaultValue="100" />
                  </div>
                  <div className="setting-item">
                    <label>Cache TTL (hours)</label>
                    <input type="number" defaultValue="24" />
                  </div>
                  <div className="setting-item">
                    <label>Max File Upload Size (MB)</label>
                    <input type="number" defaultValue="50" />
                  </div>
                  <div className="setting-item">
                    <label>Session Timeout (minutes)</label>
                    <input type="number" defaultValue="30" />
                  </div>
                </div>
                <button className="btn btn-primary">Save Settings</button>
              </div>
            )}
          </section>
        </>
      )}
    </div>
  );
}
