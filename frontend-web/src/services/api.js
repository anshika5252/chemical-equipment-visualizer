import axios from 'axios';

// Base URL for Django backend
const API_BASE_URL = 'http://127.0.0.1:8000/api';

// Create axios instance with default config
const apiClient = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

/**
 * Upload CSV file to backend
 * @param {File} file - The CSV file to upload
 * @returns {Promise} Response with dataset info
 */
export const uploadFile = async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await apiClient.post('/upload/', formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    });
    
    return response.data;
};

/**
 * Get summary of most recent dataset
 * @returns {Promise} Dataset summary with statistics
 */
export const getSummary = async () => {
    const response = await apiClient.get('/summary/');
    return response.data;
};

/**
 * Get upload history (last 5 datasets)
 * @returns {Promise} Array of datasets
 */
export const getHistory = async () => {
    const response = await apiClient.get('/history/');
    return response.data;
};

/**
 * Get specific dataset details
 * @param {number} id - Dataset ID
 * @returns {Promise} Full dataset with equipment records
 */
export const getDataset = async (id) => {
    const response = await apiClient.get(`/dataset/${id}/`);
    return response.data;
};

/**
 * Download PDF report for a dataset
 * @param {number} id - Dataset ID
 */
export const downloadReport = async (id) => {
    const response = await apiClient.get(`/report/${id}/`, {
        responseType: 'blob', // Important for file download
    });
    
    // Create download link
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `equipment_report_${id}.pdf`);
    document.body.appendChild(link);
    link.click();
    link.remove();
};

const api = {
    uploadFile,
    getSummary,
    getHistory,
    getDataset,
    downloadReport,
};

export default api;