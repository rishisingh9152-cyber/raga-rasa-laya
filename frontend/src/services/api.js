/**
 * API Service for RagaRasa Frontend
 * Handles communication with the backend with proper URL configuration
 */

// Determine API base URL based on environment
const getApiBaseUrl = () => {
  // Check if we're in production (Vercel)
  if (process.env.REACT_APP_API_URL) {
    return process.env.REACT_APP_API_URL;
  }
  
  // Check for Render backend
  if (window.location.hostname === 'raga-rasa-music-52.vercel.app' || 
      process.env.NODE_ENV === 'production') {
    return 'https://raga-rasa-backend.onrender.com';
  }
  
  // Default to localhost for development
  return 'http://127.0.0.1:8000';
};

const API_BASE_URL = getApiBaseUrl();

console.log('🌍 API Base URL:', API_BASE_URL);

/**
 * Fetch recommendations for an emotion
 * @param {string} emotion - The detected emotion
 * @param {number} limit - Number of recommendations (default: 5)
 * @returns {Promise<Array>} Array of song recommendations
 */
export const getRecommendations = async (emotion, limit = 5) => {
  try {
    const url = `${API_BASE_URL}/recommendations?emotion=${encodeURIComponent(emotion)}&limit=${limit}`;
    
    console.log('📡 Fetching recommendations from:', url);
    
    const response = await fetch(url);
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    
    const data = await response.json();
    
    console.log('✅ Recommendations received:', data);
    
    // Handle different response formats:
    // Format 1: { recommendations: [...] }
    if (data.recommendations && Array.isArray(data.recommendations)) {
      return data.recommendations;
    }
    
    // Format 2: { songs: [...] }
    if (data.songs && Array.isArray(data.songs)) {
      return data.songs;
    }
    
    // Format 3: Array directly
    if (Array.isArray(data)) {
      return data;
    }
    
    // Fallback: return empty array
    console.warn('⚠️ Unexpected API response format:', data);
    return [];
    
  } catch (error) {
    console.error('❌ Error fetching recommendations:', error);
    throw error;
  }
};

/**
 * Detect emotion using the emotion service
 * @param {Blob} imageBlob - Image blob from webcam
 * @returns {Promise<Object>} Emotion detection result
 */
export const detectEmotion = async (imageBlob) => {
  try {
    const url = `${API_BASE_URL}/emotion/live`;
    
    console.log('📡 Sending image to emotion detection:', url);
    
    const formData = new FormData();
    formData.append('file', imageBlob, 'image.jpg');
    
    const response = await fetch(url, {
      method: 'POST',
      body: formData
    });
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    
    const data = await response.json();
    
    console.log('✅ Emotion detected:', data);
    
    return data;
    
  } catch (error) {
    console.error('❌ Error detecting emotion:', error);
    throw error;
  }
};

/**
 * Get all available songs (optional - for song list)
 * @returns {Promise<Array>} Array of all songs
 */
export const getAllSongs = async () => {
  try {
    const url = `${API_BASE_URL}/songs`;
    
    console.log('📡 Fetching all songs from:', url);
    
    const response = await fetch(url);
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    
    const data = await response.json();
    
    return data.songs || [];
    
  } catch (error) {
    console.error('❌ Error fetching songs:', error);
    throw error;
  }
};

/**
 * Rate a song
 * @param {string} songId - Song ID or name
 * @param {string} userId - User ID
 * @param {number} rating - Rating value (1-5)
 * @returns {Promise<Object>} Rating result
 */
export const rateSong = async (songId, userId, rating) => {
  try {
    const url = `${API_BASE_URL}/ratings`;
    
    console.log('📡 Submitting rating to:', url);
    
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        song_name: songId,
        user_id: userId,
        rating: rating
      })
    });
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    
    const data = await response.json();
    
    console.log('✅ Rating submitted:', data);
    
    return data;
    
  } catch (error) {
    console.error('❌ Error submitting rating:', error);
    throw error;
  }
};

export default {
  getRecommendations,
  detectEmotion,
  getAllSongs,
  rateSong
};
