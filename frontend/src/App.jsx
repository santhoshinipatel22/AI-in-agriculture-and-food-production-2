import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';

// Pages
import LoginPage from './pages/LoginPage';
import Dashboard from './pages/Dashboard';
import DiseaseDetection from './pages/DiseaseDetection';
import WeatherAdvisory from './pages/WeatherAdvisory';
import PriceAnalysis from './pages/PriceAnalysis';
import IoTMonitoring from './pages/IoTMonitoring';

// Components
import Navbar from './components/Navbar';
import Chatbot from './components/Chatbot';

import './App.css';

function PrivateRoute({ children }) {
  const token = localStorage.getItem('accessToken');
  return token ? children : <Navigate to="/login" />;
}

function App() {
  return (
    <Router>
      <Toaster position="top-right" />
      
      <Routes>
        {/* Public Routes */}
        <Route path="/login" element={<LoginPage />} />

        {/* Protected Routes */}
        <Route
          path="/*"
          element={
            <PrivateRoute>
              <div className="app-layout">
                <Navbar />
                <main className="main-content">
                  <Routes>
                    <Route path="/dashboard" element={<Dashboard />} />
                    <Route path="/disease-detection" element={<DiseaseDetection />} />
                    <Route path="/weather" element={<WeatherAdvisory />} />
                    <Route path="/prices" element={<PriceAnalysis />} />
                    <Route path="/iot-monitoring" element={<IoTMonitoring />} />
                    <Route path="/chatbot" element={<Chatbot />} />
                    <Route path="/" element={<Navigate to="/dashboard" />} />
                  </Routes>
                </main>
              </div>
            </PrivateRoute>
          }
        />
      </Routes>
    </Router>
  );
}

export default App;
