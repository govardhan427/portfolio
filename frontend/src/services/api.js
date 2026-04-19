import axios from 'axios';

const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL,
    headers: { 'Content-Type': 'application/json' },
    withCredentials: true
});

// 1. Request Interceptor: Auto-attach JWT token if it exists
api.interceptors.request.use((config) => {
    const token = localStorage.getItem('access_token');
    
    // 🛑 SAFETY CHECK: Only attach the token if it is REAL.
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

// 2. Response Interceptor: Auto-clear dead tokens and silently retry
api.interceptors.response.use(
    (response) => {
        // Any status code of 2xx passes through normally
        return response;
    },
    async (error) => {
        const originalRequest = error.config;

        // Catch 401 Unauthorized errors (and ensure we don't infinitely loop)
        if (error.response && error.response.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true; // Mark as retried
            
            console.warn("Token expired or invalid. Clearing storage and retrying as guest.");
            
            // 1. Clear the bad tokens from storage
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            
            // 2. Remove the bad Authorization header from the failed request
            delete originalRequest.headers['Authorization'];
            
            // 3. Silently retry the original request as an anonymous user
            try {
                return await api(originalRequest);
            } catch (retryError) {
                // If it STILL fails after retrying without a token, 
                // it means it's a truly protected route (like the dashboard)
                if (window.location.pathname.includes('/dashboard')) {
                    window.location.href = '/'; // Kick to home/login
                }
                return Promise.reject(retryError);
            }
        }

        return Promise.reject(error);
    }
);

export default api;