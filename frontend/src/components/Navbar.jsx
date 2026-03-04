import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { FiMenu, FiX, FiLogOut, FiUser } from 'react-icons/fi';
import './Navbar.css';

export default function Navbar() {
  const [isOpen, setIsOpen] = useState(false);
  const navigate = useNavigate();
  const farmer = JSON.parse(localStorage.getItem('farmer') || '{}');

  const handleLogout = () => {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    localStorage.removeItem('farmer');
    navigate('/login');
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-logo">
          🌾 SmartFarming
        </Link>

        <div className={`nav-menu ${isOpen ? 'active' : ''}`}>
          <Link to="/dashboard" className="nav-link">
            Dashboard
          </Link>
          <Link to="/disease-detection" className="nav-link">
            Disease Detection
          </Link>
          <Link to="/weather" className="nav-link">
            Weather
          </Link>
          <Link to="/prices" className="nav-link">
            Market Prices
          </Link>
          <Link to="/iot-monitoring" className="nav-link">
            IoT Monitoring
          </Link>
          <Link to="/subsidies" className="nav-link">
            Subsidies
          </Link>
          <Link to="/chatbot" className="nav-link">
            Chatbot
          </Link>

          <div className="nav-user">
            <span className="user-name">
              <FiUser /> {farmer.firstName || 'User'}
            </span>
            <button onClick={handleLogout} className="logout-btn">
              <FiLogOut /> Logout
            </button>
          </div>
        </div>

        <div className="hamburger" onClick={() => setIsOpen(!isOpen)}>
          {isOpen ? <FiX /> : <FiMenu />}
        </div>
      </div>
    </nav>
  );
}
