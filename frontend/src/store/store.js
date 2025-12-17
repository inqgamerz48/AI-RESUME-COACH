/**
 * Global state management with Zustand
 */
import { create } from 'zustand';

const getUserFromStorage = () => {
    if (typeof window !== 'undefined') {
        return JSON.parse(localStorage.getItem('user') || 'null');
    }
    return null;
};

const getTokenFromStorage = () => {
    if (typeof window !== 'undefined') {
        return localStorage.getItem('access_token') || null;
    }
    return null;
};

export const useAuthStore = create((set) => ({
    user: getUserFromStorage(),
    token: getTokenFromStorage(),
    isAuthenticated: !!getTokenFromStorage(),

    setAuth: (user, token) => {
        if (typeof window !== 'undefined') {
            localStorage.setItem('user', JSON.stringify(user));
            localStorage.setItem('access_token', token);
        }
        set({ user, token, isAuthenticated: true });
    },

    logout: () => {
        if (typeof window !== 'undefined') {
            localStorage.removeItem('user');
            localStorage.removeItem('access_token');
        }
        set({ user: null, token: null, isAuthenticated: false });
    },
}));

export const useResumeStore = create((set) => ({
    resumes: [],
    currentResume: null,

    setResumes: (resumes) => set({ resumes }),

    setCurrentResume: (resume) => set({ currentResume: resume }),

    addResume: (resume) => set((state) => ({
        resumes: [...state.resumes, resume],
    })),

    updateResume: (id, data) => set((state) => ({
        resumes: state.resumes.map((r) => (r.id === id ? { ...r, ...data } : r)),
        currentResume: state.currentResume?.id === id
            ? { ...state.currentResume, ...data }
            : state.currentResume,
    })),

    deleteResume: (id) => set((state) => ({
        resumes: state.resumes.filter((r) => r.id !== id),
        currentResume: state.currentResume?.id === id ? null : state.currentResume,
    })),
}));

export const useUIStore = create((set) => ({
    showUpgradeModal: false,
    upgradeMessage: '',

    setShowUpgradeModal: (show, message = '') => set({
        showUpgradeModal: show,
        upgradeMessage: message,
    }),
}));
