import axios from 'axios';

const api = axios.create({
    // VITE_API_URL should be 'http://127.0.0.1:8000/api/v1' in your .env
    baseURL: import.meta.env.VITE_API_URL,
    headers: { 'Content-Type': 'application/json' },
});

// Auto-attach JWT token if it exists
api.interceptors.request.use((config) => {
    const token = localStorage.getItem('access_token');
    if (token) config.headers.Authorization = `Bearer ${token}`;
    return config;
});

export default api;