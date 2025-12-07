import api from './api';

export const getHomeData = async () => {
    const response = await api.get('/home/');
    return response.data;
};

export const getProjects = async () => {
    const response = await api.get('/projects/');
    return response.data;
};

export const getProjectDetail = async (slug) => {
    const response = await api.get(`/projects/${slug}/`);
    return response.data;
};

export const trackVisitor = async (path) => {
    // Send tracking data silently
    try {
        await api.post('/analytics/track/', {
            path: path,
            referrer: document.referrer
        });
    } catch (error) {
        console.error("Tracking failed silently", error);
    }
};
export const sendChatQuery = async (query) => {
    try {
        const response = await api.post('/features/chat/', { query });
        return response.data;
    } catch (error) {
        console.error("Chat Error", error);
        return { 
            text: "I seem to be having trouble connecting to Govardhan's mainframe. Please try again later.", 
            related_link: null 
        };
    }
};

export const sendContactMessage = async (data) => {
    // data = { name, email, message }
    const response = await api.post('/contact/', data);
    return response.data;
};