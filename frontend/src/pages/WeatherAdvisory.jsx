import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import './WeatherAdvisory.css';

export default function WeatherAdvisory({ latitude = 17.3850, longitude = 78.4867 }) {
  const [weather, setWeather] = useState(null);
  const [forecast, setForecast] = useState([]);
  const [advisory, setAdvisory] = useState(null);
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [cropType, setCropType] = useState('rice');

  const API_URL = process.env.REACT_APP_API_URL;

  useEffect(() => {
    fetchWeatherData();
  }, [latitude, longitude, cropType]);

  const fetchWeatherData = async () => {
    try {
      setLoading(true);

      const [weatherRes, forecastRes, advisoryRes, alertsRes] = await Promise.all([
        axios.get(`${API_URL}/api/weather/data`, {
          params: { latitude, longitude },
        }),
        axios.get(`${API_URL}/api/weather/forecast`, {
          params: { latitude, longitude },
        }),
        axios.get(`${API_URL}/api/weather/advisory`, {
          params: { latitude, longitude, cropType },
        }),
        axios.get(`${API_URL}/api/weather/alerts`, {
          params: { latitude, longitude },
        }),
      ]);

      setWeather(weatherRes.data.data);
      setForecast(forecastRes.data.data);
      setAdvisory(advisoryRes.data.data);
      setAlerts(alertsRes.data.data);
    } catch (error) {
      console.error('Error fetching weather data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="loading">Loading weather data...</div>;
  }

  return (
    <div className="weather-advisory">
      <h1>Real-Time Weather Advisory</h1>

      <div className="location-selector">
        <label>Crop Type:</label>
        <select value={cropType} onChange={(e) => setCropType(e.target.value)}>
          <option value="rice">Rice</option>
          <option value="wheat">Wheat</option>
          <option value="corn">Corn</option>
          <option value="cotton">Cotton</option>
        </select>
      </div>

      {/* Current Weather */}
      {weather && (
        <section className="current-weather">
          <h2>Current Weather</h2>
          <div className="weather-info">
            <div className="weather-item">
              <label>Temperature</label>
              <p>{weather.temperature}°C</p>
            </div>
            <div className="weather-item">
              <label>Humidity</label>
              <p>{weather.humidity}%</p>
            </div>
            <div className="weather-item">
              <label>Wind Speed</label>
              <p>{weather.windSpeed} m/s</p>
            </div>
            <div className="weather-item">
              <label>Rainfall</label>
              <p>{weather.rainfall} mm</p>
            </div>
            <div className="weather-item">
              <label>Condition</label>
              <p>{weather.condition}</p>
            </div>
          </div>
        </section>
      )}

      {/* Alerts */}
      {alerts.length > 0 && (
        <section className="alerts-section">
          <h2>⚠️ Weather Alerts</h2>
          {alerts.map((alert, idx) => (
            <div key={idx} className={`alert alert-${alert.severity}`}>
              <strong>{alert.type}</strong>
              <p>{alert.message}</p>
            </div>
          ))}
        </section>
      )}

      {/* Forecast */}
      <section className="forecast-section">
        <h2>10-Day Forecast</h2>
        <div className="forecast-cards">
          {forecast.slice(0, 10).map((day, idx) => (
            <div key={idx} className="forecast-card">
              <p className="date">{new Date(day.date).toLocaleDateString()}</p>
              <p className="temp">{day.temperature}°C</p>
              <p className="condition">{day.condition}</p>
              <p className="rain">💧 {day.rainfall}mm</p>
            </div>
          ))}
        </div>
      </section>

      {/* Agricultural Advisory */}
      {advisory && (
        <section className="advisory-section">
          <h2>Agricultural Advisory</h2>
          <div className="advisory-cards">
            <div className="advisory-card">
              <h4>Sowing Advisory</h4>
              <p>{advisory.sowingAdvisory}</p>
            </div>
            <div className="advisory-card">
              <h4>Irrigation Guidance</h4>
              <p>Water: {advisory.irrigationAdvisory.recommendedWater} mm</p>
              <p>Frequency: {advisory.irrigationAdvisory.frequency}</p>
              <p>Timing: {advisory.irrigationAdvisory.timing}</p>
            </div>
            <div className="advisory-card">
              <h4>Pesticide Spraying</h4>
              <p>{advisory.pesticideSprayingAdvisory}</p>
            </div>
            <div className="advisory-card">
              <h4>Best Crops for Season</h4>
              <p>{advisory.bestCropForSeason.join(', ')}</p>
            </div>
          </div>
        </section>
      )}

      {/* Map */}
      <section className="map-section">
        <h2>Farm Location</h2>
        <MapContainer center={[latitude, longitude]} zoom={12} style={{ height: '400px', width: '100%' }}>
          <TileLayer
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            attribution='&copy; OpenStreetMap contributors'
          />
          <Marker position={[latitude, longitude]}>
            <Popup>Your Farm Location</Popup>
          </Marker>
        </MapContainer>
      </section>
    </div>
  );
}
