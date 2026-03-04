import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Add token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('accessToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Handle responses and token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      try {
        const refreshToken = localStorage.getItem('refreshToken');
        const response = await axios.post(`${API_BASE_URL}/auth/refresh-token`, {
          refreshToken
        });
        localStorage.setItem('accessToken', response.data.data.accessToken);
        return api(originalRequest);
      } catch (refreshError) {
        localStorage.clear();
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }
    return Promise.reject(error);
  }
);

// Auth Services
export const authService = {
  register: (data) => api.post('/auth/register', data),
  login: (credentials) => api.post('/auth/login', credentials),
  logout: () => api.post('/auth/logout'),
  refreshToken: (refreshToken) => api.post('/auth/refresh-token', { refreshToken }),
  verifyEmail: (token) => api.get(`/auth/verify/${token}`),
  resetPassword: (email) => api.post('/auth/reset-password', { email })
};

// Crop Services
export const cropService = {
  createCrop: (data) => api.post('/crops', data),
  getAllCrops: (page = 1, limit = 20) => api.get('/crops', { params: { page, limit } }),
  getCropById: (cropId) => api.get(`/crops/${cropId}`),
  updateCrop: (cropId, data) => api.put(`/crops/${cropId}`, data),
  deleteCrop: (cropId) => api.delete(`/crops/${cropId}`),
  getCropMetrics: () => api.get('/crops/metrics'),
  getCropDiseases: (cropId) => api.get(`/crops/${cropId}/diseases`)
};

// Disease Services
export const diseaseService = {
  detectDisease: (cropId, imageFile) => {
    const formData = new FormData();
    formData.append('image', imageFile);
    return api.post(`/diseases/detect/${cropId}`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
  },
  getAllDiseases: (status = null, severity = null) => {
    const params = {};
    if (status) params.status = status;
    if (severity) params.severity = severity;
    return api.get('/diseases', { params });
  },
  updateDiseaseStatus: (diseaseId, data) => api.patch(`/diseases/${diseaseId}`, data),
  getDiseaseStats: () => api.get('/diseases/stats')
};

// Weather Services
export const weatherService = {
  getWeatherData: (lat, lon) => api.get('/weather/data', { params: { lat, lon } }),
  getForecast: (lat, lon) => api.get('/weather/forecast', { params: { lat, lon } }),
  getAdvisory: (lat, lon, cropId = null) => {
    const params = { lat, lon };
    if (cropId) params.cropId = cropId;
    return api.get('/weather/advisory', { params });
  },
  getAlerts: (lat, lon) => api.get('/weather/alerts', { params: { lat, lon } })
};

// Price Services
export const priceService = {
  getPricePrediction: (crop, region = null) => {
    const params = { crop };
    if (region) params.region = region;
    return api.get('/prices/prediction', { params });
  },
  getPriceHistory: (crop, days = 30) => api.get('/prices/history', { params: { crop, days } }),
  getMarketInsights: (region = null) => {
    const params = {};
    if (region) params.region = region;
    return api.get('/prices/insights', { params });
  }
};

// IoT Services
export const iotService = {
  registerDevice: (data) => api.post('/iot/register', data),
  getDeviceStatus: (deviceId) => api.get(`/iot/${deviceId}/status`),
  getDeviceHistory: (deviceId, days = 7, limit = 100) =>
    api.get(`/iot/${deviceId}/history`, { params: { days, limit } }),
  getLatestReadings: (deviceId) => api.get(`/iot/${deviceId}/readings`)
};

// Subsidy Services
export const subsidyService = {
  getAllSubsidies: () => api.get('/subsidies'),
  getApplicableSubsidies: () => api.get('/subsidies/applicable'),
  applyForSubsidy: (subsidyId, documents) =>
    api.post(`/subsidies/apply/${subsidyId}`, { documents }),
  getApplications: () => api.get('/subsidies/applications')
};

// Admin Services
export const adminService = {
  getStats: () => api.get('/admin/stats'),
  getSystemHealth: () => api.get('/admin/health'),
  getAllFarmers: (page = 1, limit = 20) => api.get('/admin/farmers', { params: { page, limit } }),
  uploadModel: (modelType, file) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post(`/admin/models/${modelType}`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
  }
};

export default api;
