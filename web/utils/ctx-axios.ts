import axios from 'axios';

const api = axios.create({
  baseURL: process.env.API_BASE_URL,
});

api.defaults.timeout = 10000;


api.interceptors.request.use((request) => {
    const token = localStorage.getItem("Authorization");
    if (token) {
        request.headers['Authorization'] = token
    }
    return request;
});



api.interceptors.response.use(
  response => response.data,
	err => Promise.reject(err)
);

export default api;