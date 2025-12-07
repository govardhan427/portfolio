import api from './api';

export const getFiles = async () => {
    const response = await api.get('/vault/files/');
    return response.data;
};

// 🚨 REPLACED WITH NATIVE FETCH (Simpler & Safer for Files)
export const uploadFile = async (fileObj, category) => {
    const formData = new FormData();
    formData.append('file', fileObj);
    formData.append('name', fileObj.name);
    formData.append('category', category);

    const token = localStorage.getItem('access_token');
    const url = `${import.meta.env.VITE_API_URL}/vault/files/`;

    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`,
            // NOTE: We deliberately do NOT set Content-Type here. 
            // The browser sets it to 'multipart/form-data' automatically.
        },
        body: formData
    });

    if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Upload Failed: ${response.status} ${errorText}`);
    }

    return await response.json();
};

export const deleteFile = async (id) => {
    await api.delete(`/vault/files/${id}/`);
};