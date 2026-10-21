import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for adding auth token
api.interceptors.request.use(
  (config) => {
    const user = localStorage.getItem('user');
    if (user) {
      try {
        const userData = JSON.parse(user);
        // Add token if available (implement when backend provides tokens)
        // config.headers.Authorization = `Bearer ${userData.token}`;
      } catch (error) {
        console.error('Error parsing user data:', error);
      }
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for handling errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Unauthorized - clear user data and redirect to login
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const authService = {
  // SSO Login - implement based on your SSO provider
  ssoLogin: async (email) => {
    // TODO: Implement actual SSO login
    // This is a placeholder - replace with actual SSO implementation
    return api.post('/auth/sso', { email });
  },

  // Logout
  logout: async () => {
    return api.post('/auth/logout');
  },

  // Verify token/session
  verifySession: async () => {
    return api.get('/auth/verify');
  },
};

export const userService = {
  getProfile: async () => {
    return api.get('/users/me');
  },

  updateProfile: async (data) => {
    return api.put('/users/me', data);
  },
};

export default api;
