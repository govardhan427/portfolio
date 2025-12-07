import api from './api';

export const getBlogPosts = async () => {
    const response = await api.get('/blog/posts/');
    return response.data;
};

export const getBlogPostBySlug = async (slug) => {
    const response = await api.get(`/blog/posts/${slug}/`);
    return response.data;
};