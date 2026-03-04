import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import './PriceAnalysis.css';

export default function PriceAnalysis() {
  const [cropName, setCropName] = useState('rice');
  const [region, setRegion] = useState('Telangana');
  const [prediction, setPrediction] = useState(null);
  const [history, setHistory] = useState([]);
  const [insights, setInsights] = useState(null);
  const [loading, setLoading] = useState(false);

  const API_URL = process.env.REACT_APP_API_URL;

  useEffect(() => {
    fetchPriceData();
  }, [cropName, region]);

  const fetchPriceData = async () => {
    try {
      setLoading(true);

      const [predictionRes, historyRes, insightsRes] = await Promise.all([
        axios.get(`${API_URL}/api/prices/prediction`, {
          params: { cropName, region },
        }),
        axios.get(`${API_URL}/api/prices/history`, {
          params: { cropName, days: 30 },
        }),
        axios.get(`${API_URL}/api/prices/insights`, {
          params: { cropName, region },
        }),
      ]);

      setPrediction(predictionRes.data.data);
      setHistory(historyRes.data.data);
      setInsights(insightsRes.data.data);
    } catch (error) {
      console.error('Error fetching price data:', error);
    } finally {
      setLoading(false);
    }
  };

  const mockHistoryChart = [
    { date: '2024-01-01', price: 2400 },
    { date: '2024-01-05', price: 2500 },
    { date: '2024-01-10', price: 2450 },
    { date: '2024-01-15', price: 2600 },
    { date: '2024-01-20', price: 2550 },
    { date: '2024-01-25', price: 2700 },
    { date: '2024-02-01', price: 2650 },
  ];

  if (loading) {
    return <div className="loading">Loading price data...</div>;
  }

  return (
    <div className="price-analysis">
      <h1>AI-Powered Crop Price Prediction</h1>
      <p>Smart market timing for maximum profit</p>

      <div className="selector-section">
        <div className="form-group">
          <label>Crop</label>
          <select value={cropName} onChange={(e) => setCropName(e.target.value)}>
            <option value="rice">Rice</option>
            <option value="wheat">Wheat</option>
            <option value="corn">Corn</option>
          </select>
        </div>
        <div className="form-group">
          <label>Region</label>
          <select value={region} onChange={(e) => setRegion(e.target.value)}>
            <option value="Telangana">Telangana</option>
            <option value="AndhraPradesh">Andhra Pradesh</option>
            <option value="Karnataka">Karnataka</option>
          </select>
        </div>
      </div>

      {/* Current Price & Prediction */}
      {prediction && (
        <section className="price-prediction">
          <h2>Price Prediction</h2>
          <div className="prediction-cards">
            <div className="card current-price">
              <h4>Current Price</h4>
              <p className="price">₹{prediction.currentPrice}/quintal</p>
            </div>
            <div className={`card predicted-price ${prediction.trend}`}>
              <h4>Predicted Price (7 days)</h4>
              <p className="price">₹{prediction.predictedPrice}/quintal</p>
              <p className="trend">{prediction.trend.toUpperCase()}</p>
            </div>
            <div className="card confidence">
              <h4>Confidence</h4>
              <p className="percentage">{prediction.confidence}%</p>
            </div>
            <div className={`card recommendation ${prediction.recommendation.action}`}>
              <h4>Recommendation</h4>
              <p className="action">{prediction.recommendation.action.toUpperCase()}</p>
              <p className="reason">{prediction.recommendation.reasoning}</p>
              <p className="profit">{{expected_profit}}: ₹{prediction.recommendation.expectedProfit}</p>
            </div>
          </div>

          <div className="best-sell-date">
            <p>Best time to sell: <strong>{new Date(prediction.recommendation.bestSellDate).toLocaleDateString()}</strong></p>
          </div>
        </section>
      )}

      {/* Price History Chart */}
      <section className="price-history">
        <h2>30-Day Price Trend</h2>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={mockHistoryChart}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line 
              type="monotone" 
              dataKey="price" 
              stroke="#4CAF50" 
              connectNulls 
              name="Price (₹/quintal)"
            />
          </LineChart>
        </ResponsiveContainer>
      </section>

      {/* Market Insights */}
      {insights && (
        <section className="market-insights">
          <h2>Market Insights</h2>
          <div className="insights-grid">
            <div className="insight-card">
              <h4>Average Price</h4>
              <p className="value">₹{insights.averagePrice?.toFixed(0)}</p>
            </div>
            <div className="insight-card">
              <h4>Min Price</h4>
              <p className="value">₹{insights.minPrice?.toFixed(0)}</p>
            </div>
            <div className="insight-card">
              <h4>Max Price</h4>
              <p className="value">₹{insights.maxPrice?.toFixed(0)}</p>
            </div>
            <div className="insight-card">
              <h4>Current Trend</h4>
              <p className="value">{insights.currentTrend}</p>
            </div>
          </div>
        </section>
      )}

      {/* Tips */}
      <section className="tips-section">
        <h2>💡 Smart Selling Tips</h2>
        <div className="tips">
          <div className="tip">
            <h4>Monitor Prices Daily</h4>
            <p>Check market rates every morning to make informed decisions</p>
          </div>
          <div className="tip">
            <h4>Storage is Investment</h4>
            <p>Store crops during low prices to sell when prices spike</p>
          </div>
          <div className="tip">
            <h4>Diversify Crops</h4>
            <p>Grow multiple crops to balance market risk</p>
          </div>
          <div className="tip">
            <h4>Use Direct Markets</h4>
            <p>Sell directly to buyers to maximize profit margin</p>
          </div>
        </div>
      </section>
    </div>
  );
}
