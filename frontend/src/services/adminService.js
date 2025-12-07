import api from './api';

export const getDashboardStats = async () => {
    try {
        const response = await api.get('/analytics/dashboard/');
        return response.data;
    } catch (error) {
        console.error("Failed to fetch dashboard stats", error);
        throw error;
    }
};

export const getRecentVisitors = async () => {
    try {
        const response = await api.get('/analytics/visitors/');
        return response.data;
    } catch (error) {
        console.error("Failed to fetch visitors", error);
        throw error;
    }
};