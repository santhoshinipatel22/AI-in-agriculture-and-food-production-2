import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  LineChart, Line, BarChart, Bar, PieChart, Pie, Cell,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from 'recharts';
import './Dashboard.css';

export default function Dashboard() {
  const [farmerData, setFarmerData] = useState(null);
  const [crops, setCrops] = useState([]);
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('overview');

  const API_URL = process.env.REACT_APP_API_URL;
  const token = localStorage.getItem('accessToken');

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const headers = {
        Authorization: `Bearer ${token}`,
      };

      const [farmerRes, cropsRes, metricsRes] = await Promise.all([
        axios.get(`${API_URL}/api/auth/profile`, { headers }),
        axios.get(`${API_URL}/api/crops`, { headers }),
        axios.get(`${API_URL}/api/crops/metrics`, { headers }),
      ]);

      setFarmerData(farmerRes.data.data);
      setCrops(cropsRes.data.data);
      setMetrics(metricsRes.data.data);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  const mockChartData = [
    { month: 'Jan', yield: 4000, expenses: 2400 },
    { month: 'Feb', yield: 4500, expenses: 2800 },
    { month: 'Mar', yield: 5000, expenses: 3000 },
    { month: 'Apr', yield: 6000, expenses: 3200 },
    { month: 'May', yield: 5800, expenses: 3500 },
    { month: 'Jun', yield: 7000, expenses: 4000 },
  ];

  if (loading) {
    return <div className="loading">Loading dashboard...</div>;
  }

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h1>Welcome, {farmerData?.firstName}!</h1>
        <p>{farmerData?.farmName} • {farmerData?.farmLocation?.district}</p>
      </header>

      {/* Key Metrics */}
      <section className="metrics-section">
        <div className="metric-card">
          <h3>Active Crops</h3>
          <p className="metric-value">{metrics?.activeCrops || 0}</p>
        </div>
        <div className="metric-card">
          <h3>Total Yield</h3>
          <p className="metric-value">{metrics?.totalYield?.toFixed(0) || 0} kg</p>
        </div>
        <div className="metric-card">
          <h3>Total Expenses</h3>
          <p className="metric-value">₹{metrics?.totalExpense?.toLocaleString() || 0}</p>
        </div>
        <div className="metric-card">
          <h3>Estimated Profit</h3>
          <p className="metric-value">₹{(farmerData?.totalProfit || 0).toLocaleString()}</p>
        </div>
      </section>

      {/* Tabs */}
      <section className="tab-section">
        <div className="tabs">
          <button 
            className={`tab-btn ${activeTab === 'overview' ? 'active' : ''}`}
            onClick={() => setActiveTab('overview')}
          >
            Overview
          </button>
          <button 
            className={`tab-btn ${activeTab === 'crops' ? 'active' : ''}`}
            onClick={() => setActiveTab('crops')}
          >
            Crops
          </button>
          <button 
            className={`tab-btn ${activeTab === 'analytics' ? 'active' : ''}`}
            onClick={() => setActiveTab('analytics')}
          >
            Analytics
          </button>
        </div>

        {/* Overview Tab */}
        {activeTab === 'overview' && (
          <div className="tab-content">
            <div className="cards-grid">
              <div className="info-card">
                <h3>Farm Location</h3>
                <p>{farmerData?.farmLocation?.address}</p>
                <p>{farmerData?.farmLocation?.pinCode}</p>
              </div>
              <div className="info-card">
                <h3>Farm Size</h3>
                <p>{farmerData?.farmSize} hectares</p>
              </div>
              <div className="info-card">
                <h3>Subscription</h3>
                <p>{farmerData?.subscriptionPlan}</p>
              </div>
              <div className="info-card">
                <h3>Preferred Language</h3>
                <p>{farmerData?.language}</p>
              </div>
            </div>
          </div>
        )}

        {/* Crops Tab */}
        {activeTab === 'crops' && (
          <div className="tab-content">
            <div className="crops-list">
              {crops.map((crop) => (
                <div key={crop._id} className="crop-card">
                  <div className="crop-header">
                    <h4>{crop.cropName}</h4>
                    <span className={`status ${crop.status}`}>{crop.status}</span>
                  </div>
                  <p>Field: {crop.fieldName} ({crop.fieldArea} ha)</p>
                  <p>Sown: {new Date(crop.sowingDate).toLocaleDateString()}</p>
                  <p>Expected Harvest: {new Date(crop.expectedHarvestDate).toLocaleDateString()}</p>
                  <p>Estimated Yield: {crop.estimatedYield} kg/ha</p>
                </div>
              ))}
              {crops.length === 0 && (
                <p className="no-data">No crops added yet. <a href="/add-crop">Add your first crop</a></p>
              )}
            </div>
          </div>
        )}

        {/* Analytics Tab */}
        {activeTab === 'analytics' && (
          <div className="tab-content">
            <div className="charts-container">
              <div className="chart">
                <h3>Yield vs Expenses</h3>
                <ResponsiveContainer width="100%" height={300}>
                  <LineChart data={mockChartData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="month" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Line type="monotone" dataKey="yield" stroke="#4CAF50" />
                    <Line type="monotone" dataKey="expenses" stroke="#FF9800" />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>
        )}
      </section>
    </div>
  );
}
