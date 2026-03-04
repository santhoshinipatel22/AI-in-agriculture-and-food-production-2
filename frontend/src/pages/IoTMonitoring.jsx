import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './IoTMonitoring.css';

export default function IoTMonitoring() {
  const [devices, setDevices] = useState([]);
  const [selectedDevice, setSelectedDevice] = useState(null);
  const [deviceData, setDeviceData] = useState(null);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);

  const API_URL = process.env.REACT_APP_API_URL;
  const token = localStorage.getItem('accessToken');

  useEffect(() => {
    fetchDevices();
  }, []);

  const fetchDevices = async () => {
    try {
      const response = await axios.get(
        `${API_URL}/api/iot`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      setDevices(response.data.data);
      if (response.data.data.length > 0) {
        setSelectedDevice(response.data.data[0]._id);
      }
    } catch (error) {
      console.error('Error fetching devices:', error);
    }
  };

  const fetchDeviceData = async (deviceId) => {
    try {
      setLoading(true);
      const [statusRes, historyRes] = await Promise.all([
        axios.get(
          `${API_URL}/api/iot/${deviceId}/status`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        ),
        axios.get(
          `${API_URL}/api/iot/${deviceId}/history?hours=24`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        ),
      ]);

      setDeviceData(statusRes.data.data);
      setHistory(historyRes.data.data);
    } catch (error) {
      console.error('Error fetching device data:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (selectedDevice) {
      fetchDeviceData(selectedDevice);
    }
  }, [selectedDevice]);

  return (
    <div className="iot-monitoring">
      <h1>IoT Sensor Monitoring</h1>
      <p>Real-time soil and environmental data from your fields</p>

      <div className="monitoring-container">
        {/* Device List */}
        <section className="devices-section">
          <h2>Connected Devices</h2>
          <div className="device-list">
            {devices.map((device) => (
              <div
                key={device._id}
                className={`device-item ${selectedDevice === device._id ? 'active' : ''}`}
                onClick={() => setSelectedDevice(device._id)}
              >
                <div className={`status-indicator ${device.status}`}></div>
                <div className="device-info">
                  <p className="device-name">{device.deviceName}</p>
                  <p className="device-type">{device.deviceType.replace('_', ' ')}</p>
                  <p className="device-location">{device.fieldName}</p>
                </div>
              </div>
            ))}
            {devices.length === 0 && (
              <p className="no-devices">No IoT devices connected. <a href="/add-device">Add device</a></p>
            )}
          </div>
        </section>

        {/* Device Data */}
        {deviceData && (
          <section className="device-data-section">
            <h2>Current Readings</h2>

            {!loading ? (
              <>
                <div className="readings-grid">
                  <div className="reading-card">
                    <label>Soil Moisture</label>
                    <p className="value">{deviceData.latestReadings.soilMoisture}%</p>
                    <p className="status">
                      {deviceData.latestReadings.soilMoisture < 30 ? '🔴 Low' :
                       deviceData.latestReadings.soilMoisture > 80 ? '🟡 High' : '🟢 Optimal'}
                    </p>
                  </div>

                  <div className="reading-card">
                    <label>Temperature</label>
                    <p className="value">{deviceData.latestReadings.temperature}°C</p>
                    <p className="unit">Celsius</p>
                  </div>

                  <div className="reading-card">
                    <label>Humidity</label>
                    <p className="value">{deviceData.latestReadings.humidity}%</p>
                    <p className="unit">Relative Humidity</p>
                  </div>

                  <div className="reading-card">
                    <label>Soil pH</label>
                    <p className="value">{deviceData.latestReadings.ph}</p>
                    <p className="status">
                      {deviceData.latestReadings.ph < 6 ? '🔴 Acidic' :
                       deviceData.latestReadings.ph > 7.5 ? '🟡 Alkaline' : '🟢 Normal'}
                    </p>
                  </div>

                  <div className="reading-card">
                    <label>EC (Conductivity)</label>
                    <p className="value">{deviceData.latestReadings.ec} dS/m</p>
                  </div>

                  <div className="reading-card">
                    <label>Battery Level</label>
                    <p className="value">{deviceData.batteryLevel}%</p>
                    <div className="battery-bar" style={{ width: `${deviceData.batteryLevel}%` }}></div>
                  </div>
                </div>

                {/* Alerts */}
                {history.some(h => h.alerts?.length > 0) && (
                  <div className="alerts-section">
                    <h3>⚠️ Active Alerts</h3>
                    <div className="alerts-list">
                      {history.map((reading) => reading.alerts?.map((alert, idx) => (
                        <div key={idx} className={`alert alert-${alert.severity}`}>
                          <strong>{alert.type}</strong>
                          <p>{alert.message}</p>
                        </div>
                      )))}
                    </div>
                  </div>
                )}

                {/* Device Info */}
                <div className="device-info-section">
                  <h3>Device Information</h3>
                  <p><strong>Device ID:</strong> {deviceData.deviceId}</p>
                  <p><strong>Last Updated:</strong> {new Date(deviceData.latestReadings.timestamp).toLocaleString()}</p>
                  <p><strong>Status:</strong> {deviceData.status}</p>
                </div>
              </>
            ) : (
              <div className="loading">Loading device data...</div>
            )}
          </section>
        )}
      </div>
    </div>
  );
}
