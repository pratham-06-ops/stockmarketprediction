import axios from 'axios';

// Base API configuration
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:5000';

// Create axios instance with default configuration
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Clear auth token on unauthorized
      localStorage.removeItem('authToken');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Authentication APIs
export const authAPI = {
  login: async (credentials) => {
    const response = await api.post('/api/login', credentials);
    return response.data;
  },
  
  register: async (userData) => {
    const response = await api.post('/api/register', userData);
    return response.data;
  },
  
  logout: async () => {
    const response = await api.post('/api/logout');
    localStorage.removeItem('authToken');
    localStorage.removeItem('user');
    return response.data;
  },
  
  changePassword: async (passwordData) => {
    const response = await api.post('/api/change-password', passwordData);
    return response.data;
  }
};

// Stock Data APIs
export const stockAPI = {
  getCompanies: async () => {
    const response = await api.get('/api/companies');
    return response.data;
  },
  
  getStockData: async (company, period = '1y') => {
    const response = await api.get(`/api/stock-data/${company}`, {
      params: { period }
    });
    return response.data;
  },
  
  predict: async (predictionData) => {
    const response = await api.post('/api/predict', predictionData);
    return response.data;
  },
  
  getPredictionHistory: async () => {
    const response = await api.get('/api/predictions/history');
    return response.data;
  }
};

// Admin APIs
export const adminAPI = {
  getUsers: async () => {
    const response = await api.get('/api/admin/users');
    return response.data;
  },
  
  getStatistics: async () => {
    const response = await api.get('/api/admin/statistics');
    return response.data;
  }
};

// Utility function to check API connection
export const checkAPIConnection = async () => {
  try {
    const response = await api.get('/api/companies');
    return { connected: true, message: 'API connection successful' };
  } catch (error) {
    return { 
      connected: false, 
      message: error.message || 'Failed to connect to API',
      details: error.response?.data?.message || 'Backend server may be down'
    };
  }
};

export default api;