import axios from 'axios';

const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getHealth = async () => {
  try {
    const res = await api.get('/api/health');
    return res.data;
  } catch (err) {
    throw err;
  }
};

export const sendChat = async (payload: any) => {
  try {
    const res = await api.post('/api/chat', payload);
    return res.data;
  } catch (err) {
    throw err;
  }
};

export const analyzeLog = async (payload: any) => {
  try {
    const res = await api.post('/api/logs/analyze', payload);
    return res.data;
  } catch (err) {
    throw err;
  }
};

export const searchDocs = async (query: string) => {
  try {
    const res = await api.get(`/api/docs/search?query=${encodeURIComponent(query)}`);
    return res.data;
  } catch (err) {
    throw err;
  }
};

export default api;
