/**
 * React Integration Example for Emotion Detection API
 * 
 * This file shows how to integrate the BERT emotion detection model
 * with your React frontend for the mental health coaching AI
 */

import React, { useState, useEffect } from 'react';
import axios from 'axios';

// API Configuration
const API_BASE_URL = 'http://localhost:5000/api';

/**
 * Hook for emotion detection
 */
export const useEmotionDetection = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const detectEmotion = async (text) => {
    setLoading(true);
    setError(null);

    try {
      const response = await axios.post(`${API_BASE_URL}/predict`, {
        text: text
      });

      setLoading(false);
      return response.data;
    } catch (err) {
      setError(err.message);
      setLoading(false);
      return null;
    }
  };

  return { detectEmotion, loading, error };
};

/**
 * Emotion Detection Component
 */
export const EmotionDetector = ({ text, onEmotionDetected }) => {
  const [emotion, setEmotion] = useState(null);
  const { detectEmotion, loading, error } = useEmotionDetection();

  useEffect(() => {
    if (text && text.length > 3) {
      // Detect emotion when text changes
      const timer = setTimeout(() => {
        detectEmotion(text).then(result => {
          if (result) {
            setEmotion(result);
            if (onEmotionDetected) {
              onEmotionDetected(result);
            }
          }
        });
      }, 1000); // Debounce for 1 second

      return () => clearTimeout(timer);
    }
  }, [text]);

  if (loading) {
    return <div className="emotion-loading">Analyzing emotion...</div>;
  }

  if (error) {
    return <div className="emotion-error">Error: {error}</div>;
  }

  if (!emotion) {
    return null;
  }

  return (
    <div className="emotion-result">
      <div className="top-emotion">
        <span className="emotion-label">{emotion.top_emotion}</span>
        <span className="confidence">
          {(emotion.top_confidence * 100).toFixed(1)}%
        </span>
      </div>
      
      {emotion.detected_emotions && emotion.detected_emotions.length > 0 && (
        <div className="other-emotions">
          {emotion.detected_emotions.slice(0, 3).map((e, idx) => (
            <span key={idx} className="emotion-tag">
              {e.emotion} ({(e.confidence * 100).toFixed(1)}%)
            </span>
          ))}
        </div>
      )}
    </div>
  );
};

/**
 * Chat Component with Emotion Detection
 */
export const EmotionAwareChat = () => {
  const [messages, setMessages] = useState([]);
  const [currentMessage, setCurrentMessage] = useState('');
  const [currentEmotion, setCurrentEmotion] = useState(null);
  const { detectEmotion } = useEmotionDetection();

  const handleSendMessage = async () => {
    if (!currentMessage.trim()) return;

    // Detect emotion before sending
    const emotionResult = await detectEmotion(currentMessage);

    const newMessage = {
      text: currentMessage,
      sender: 'user',
      timestamp: new Date(),
      emotion: emotionResult ? emotionResult.top_emotion : 'neutral',
      emotionConfidence: emotionResult ? emotionResult.top_confidence : 0,
      responseApproach: emotionResult ? emotionResult.response_approach : null
    };

    setMessages([...messages, newMessage]);
    setCurrentMessage('');
    setCurrentEmotion(null);

    // Generate AI response based on detected emotion
    generateAIResponse(newMessage);
  };

  const generateAIResponse = (userMessage) => {
    // Use emotion-aware response generation
    const responseTemplates = {
      sadness: "I hear that you're feeling down. Would you like to talk about what's contributing to these feelings?",
      anger: "I understand you're feeling frustrated. It's okay to feel angry. Can you tell me more about what triggered this?",
      fear: "It sounds like you're experiencing some anxiety. Let's take this step by step. What's worrying you most?",
      joy: "That's wonderful to hear! It's great that you're experiencing positive emotions. What's bringing you joy?",
      confusion: "It seems like things feel unclear right now. Let's work through this together. What's most confusing?",
      neutral: "I'm here to listen. What would you like to talk about today?"
    };

    const response = responseTemplates[userMessage.emotion] || responseTemplates.neutral;

    setTimeout(() => {
      const aiMessage = {
        text: response,
        sender: 'ai',
        timestamp: new Date(),
        respondingToEmotion: userMessage.emotion
      };
      setMessages(prev => [...prev, aiMessage]);
    }, 1000);
  };

  return (
    <div className="emotion-aware-chat">
      <div className="chat-messages">
        {messages.map((msg, idx) => (
          <div key={idx} className={`message message-${msg.sender}`}>
            <div className="message-text">{msg.text}</div>
            {msg.emotion && (
              <div className="message-emotion">
                Detected: {msg.emotion} ({(msg.emotionConfidence * 100).toFixed(0)}%)
              </div>
            )}
          </div>
        ))}
      </div>

      <div className="chat-input-container">
        {currentEmotion && (
          <EmotionDetector 
            text={currentMessage}
            onEmotionDetected={setCurrentEmotion}
          />
        )}
        
        <div className="chat-input">
          <input
            type="text"
            value={currentMessage}
            onChange={(e) => setCurrentMessage(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
            placeholder="Type your message..."
          />
          <button onClick={handleSendMessage}>Send</button>
        </div>
      </div>
    </div>
  );
};

/**
 * Dashboard Component - Shows emotion statistics
 */
export const EmotionDashboard = ({ conversationId }) => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch conversation emotion statistics
    fetchEmotionStats(conversationId);
  }, [conversationId]);

  const fetchEmotionStats = async (convId) => {
    // This would call your backend API that aggregates emotions
    // For now, this is a placeholder
    setLoading(false);
  };

  return (
    <div className="emotion-dashboard">
      <h3>Emotion Analysis</h3>
      <div className="emotion-chart">
        {/* Add emotion distribution chart here */}
      </div>
    </div>
  );
};

/**
 * API Service Class
 */
export class EmotionDetectionAPI {
  constructor(baseURL = 'http://localhost:5000/api') {
    this.baseURL = baseURL;
    this.client = axios.create({
      baseURL: this.baseURL,
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json'
      }
    });
  }

  async predict(text) {
    try {
      const response = await this.client.post('/predict', { text });
      return response.data;
    } catch (error) {
      console.error('Emotion prediction error:', error);
      throw error;
    }
  }

  async predictBatch(texts) {
    try {
      const response = await this.client.post('/predict/batch', { texts });
      return response.data.predictions;
    } catch (error) {
      console.error('Batch prediction error:', error);
      throw error;
    }
  }

  async getEmotions() {
    try {
      const response = await this.client.get('/emotions');
      return response.data.emotions;
    } catch (error) {
      console.error('Get emotions error:', error);
      throw error;
    }
  }

  async healthCheck() {
    try {
      const response = await this.client.get('/health');
      return response.data;
    } catch (error) {
      console.error('Health check error:', error);
      throw error;
    }
  }
}

/**
 * Example Usage in App.js
 */
export const ExampleApp = () => {
  const [apiStatus, setApiStatus] = useState('checking');
  const api = new EmotionDetectionAPI();

  useEffect(() => {
    // Check API health on mount
    api.healthCheck()
      .then(() => setApiStatus('connected'))
      .catch(() => setApiStatus('disconnected'));
  }, []);

  return (
    <div className="app">
      <header>
        <h1>Mental Health Coaching AI</h1>
        <div className={`api-status ${apiStatus}`}>
          API: {apiStatus}
        </div>
      </header>

      <main>
        <EmotionAwareChat />
      </main>
    </div>
  );
};

/**
 * CSS Styles (emotion-detection.css)
 */
export const emotionDetectionStyles = `
.emotion-result {
  padding: 10px;
  background: #f0f8ff;
  border-radius: 8px;
  margin: 10px 0;
}

.top-emotion {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 16px;
  font-weight: bold;
}

.emotion-label {
  color: #2c3e50;
  text-transform: capitalize;
}

.confidence {
  color: #27ae60;
  font-size: 14px;
}

.other-emotions {
  display: flex;
  gap: 8px;
  margin-top: 8px;
  flex-wrap: wrap;
}

.emotion-tag {
  background: #e8f4f8;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 12px;
  color: #34495e;
}

.message {
  padding: 12px;
  margin: 8px 0;
  border-radius: 8px;
  max-width: 70%;
}

.message-user {
  background: #007bff;
  color: white;
  margin-left: auto;
}

.message-ai {
  background: #f1f3f5;
  color: #212529;
}

.message-emotion {
  font-size: 11px;
  margin-top: 4px;
  opacity: 0.7;
}

.api-status {
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
}

.api-status.connected {
  background: #d4edda;
  color: #155724;
}

.api-status.disconnected {
  background: #f8d7da;
  color: #721c24;
}

.api-status.checking {
  background: #fff3cd;
  color: #856404;
}
`;

// Export default
export default {
  useEmotionDetection,
  EmotionDetector,
  EmotionAwareChat,
  EmotionDashboard,
  EmotionDetectionAPI,
  ExampleApp
};
