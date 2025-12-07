import api from './api';

export const login = async (username, password) => {
    try {
        // 1. Send credentials to Django
        const response = await api.post('/token/', { username, password });
        
        // 2. If successful, Django sends { access: "...", refresh: "..." }
        if (response.data.access) {
            localStorage.setItem('access_token', response.data.access);
            localStorage.setItem('refresh_token', response.data.refresh);
            return true;
        }
    } catch (error) {
        console.error("Login Failed:", error);
        throw error; // Let the UI know it failed
    }
};

export const logout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    window.location.href = '/'; // Hard redirect to home
};

export const isAuthenticated = () => {
    // Simple check: do we have a token?
    // In a real app, we would verify token expiry here.
    return !!localStorage.getItem('access_token');
};