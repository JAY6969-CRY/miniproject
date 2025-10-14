import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getQuote = async (symbol) => {
  const response = await api.get('/quote', { params: { symbol } });
  return response.data;
};

export const getPrediction = async (symbol) => {
  const response = await api.get('/predict', { params: { symbol } });
  return response.data;
};

export const getSignal = async (symbol) => {
  const response = await api.get('/signal', { params: { symbol } });
  return response.data;
};

export const getChartData = async (symbol) => {
  const response = await api.get('/chart', { params: { symbol } });
  return response.data;
};

export const getPortfolioSignal = async (symbol, type = 'balanced') => {
  const response = await api.get('/portfolio', { params: { symbol, type } });
  return response.data;
};

export default api;
