import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
const API_V1 = '/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL + API_V1,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Handle token expiration
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const authApi = {
  login: (email, password) =>
    api.post('/auth/login', new URLSearchParams({
      username: email,
      password: password,
    }), {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    }),
  register: (userData) => api.post('/auth/register', userData),
  logout: () => {
    localStorage.removeItem('access_token');
    window.location.href = '/login';
  }
};

export const userApi = {
  getMe: () => api.get('/users/me'),
  updateMe: (userData) => api.put('/users/me', userData),
  getAll: () => api.get('/users/'),
  getById: (id) => api.get(`/users/${id}`),
};

export const itemsApi = {
  getAll: (page = 1, pageSize = 10) =>
    api.get('/items/', { params: { page, page_size: pageSize } }),
  getById: (id) => api.get(`/items/${id}`),
  create: (item) => api.post('/items/', item),
  update: (id, item) => api.put(`/items/${id}`, item),
  delete: (id) => api.delete(`/items/${id}`),
};

export default api;