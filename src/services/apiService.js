import axios from 'axios';

// Base URL for the Flask backend
const API_BASE_URL = 'http://127.0.0.1:5000';

// Function to send form data to the backend
export const sendFormData = async (formData) => {
    try {
        const response = await axios.post(`${API_BASE_URL}/submit-data`, formData);
        return response.data;
    } catch (error) {
        console.error('Error sending form data:', error); // Log error details for debugging
        throw error; // Throw the error to be handled by the frontend
    }
};




