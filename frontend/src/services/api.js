/**
 * API Service - Centralized HTTP client
 */
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Add auth token to requests
api.interceptors.request.use((config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

// Handle 401 errors
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            localStorage.removeItem('access_token');
            localStorage.removeItem('user');
            window.location.href = '/login';
        }
        return Promise.reject(error);
    }
);

export const authService = {
    register: async (email, password, fullName) => {
        const response = await api.post('/api/v1/auth/register', {
            email,
            password,
            full_name: fullName,
        });
        return response.data;
    },

    login: async (email, password) => {
        const response = await api.post('/api/v1/auth/login', { email, password });
        return response.data;
    },
};

export const aiService = {
    rewriteBullet: async (text, tone = 'professional') => {
        const response = await api.post('/api/v1/chat/rewrite', { text, tone });
        return response.data;
    },

    generateProject: async (projectName, techStack, keyPoints) => {
        const response = await api.post('/api/v1/chat/project', {
            project_name: projectName,
            tech_stack: techStack,
            key_points: keyPoints,
        });
        return response.data;
    },

    generateSummary: async (skills, experience, goal) => {
        const response = await api.post('/api/v1/chat/summary', {
            skills,
            experience,
            goal,
        });
        return response.data;
    },
};

export const resumeService = {
    createResume: async (resumeData) => {
        const response = await api.post('/api/v1/resume', resumeData);
        return response.data;
    },

    getResumes: async () => {
        const response = await api.get('/api/v1/resume');
        return response.data;
    },

    getResume: async (id) => {
        const response = await api.get(`/api/v1/resume/${id}`);
        return response.data;
    },

    updateResume: async (id, data) => {
        const response = await api.put(`/api/v1/resume/${id}`, data);
        return response.data;
    },

    deleteResume: async (id) => {
        await api.delete(`/api/v1/resume/${id}`);
    },

    exportPDF: async (id) => {
        const response = await api.get(`/api/v1/resume/${id}/pdf`, {
            responseType: 'blob',
        });
        return response.data;
    },
};

export const billingService = {
    getPlans: async () => {
        const response = await api.get('/api/v1/billing/plans');
        return response.data;
    },

    // PLACEHOLDER - Not implemented in MVP
    upgradePlan: async (plan, paymentMethod) => {
        const response = await api.post('/api/v1/billing/upgrade', {
            plan,
            payment_method: paymentMethod,
        });
        return response.data;
    },
};

export default api;
