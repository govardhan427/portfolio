import axios from 'axios';

const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL,
    headers: { 'Content-Type': 'application/json' },
    withCredentials: true
});

// Auto-attach JWT token if it exists
api.interceptors.request.use((config) => {
    const token = localStorage.getItem('access_token');
    
    // 🛑 SAFETY CHECK:
    // Only attach the token if it is REAL.
    // This prevents sending "Bearer null" or "Bearer undefined", which causes 401 errors.
    if (token && token !== "null" && token !== "undefined") {
        config.headers.Authorization = `Bearer ${token}`;
    } else {
        // Explicitly delete the header to ensure we are treated as a "Guest"
        delete config.headers.Authorization;
    }
    
    return config;
}, (error) => {
    return Promise.reject(error);
});

export default api;