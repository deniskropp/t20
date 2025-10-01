import axios from 'axios';

// Use the API URL from environment variables for production, fallback to default for development
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const fetchModels = async () => {
  try {
    const response = await apiClient.get('/models');
    return response.data;
  } catch (error) {
    console.error('Error fetching models:', error.response?.data || error.message);
    throw error;
  }
};

export const searchByText = async (query, modelName) => {
  try {
    const response = await apiClient.post('/benchmark/text', {
      query: query,
      model_name: modelName,
    });
    return response.data.results;
  } catch (error) {
    console.error('Error searching by text:', error.response?.data || error.message);
    throw error;
  }
};

export const searchByImage = async (imageBase64, modelName) => {
  try {
    const response = await apiClient.post('/benchmark/image', {
      image_base64: imageBase64,
      model_name: modelName,
    });
    return response.data.results;
  } catch (error) {
    console.error('Error searching by image:', error.response?.data || error.message);
    throw error;
  }
};

export const indexImage = async (imageBase64, metadata, modelName) => {
  // Note: The backend's index_image endpoint currently doesn't take modelName, 
  // but it's included here for potential future use or if the backend is updated.
  // The metadata object should be structured as expected by the backend.
  try {
    const response = await apiClient.post('/index_image', {
      image_base64: imageBase64,
      metadata: metadata,
    });
    return response.data; // Expected to return {'message': '...', 'image_id': '...'}
  } catch (error) {
    console.error('Error indexing image:', error.response?.data || error.message);
    throw error;
  }
};
