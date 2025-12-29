"""
Flask API Server for Emotion Detection
For integration with React frontend
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
import json
import os
import numpy as np

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Global predictor variable
predictor = None


class EmotionPredictor:
    """Real-time emotion prediction"""
    
    def __init__(self, model_path, config_path):
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        self.emotions = self.config['emotions']
        self.num_emotions = self.config['num_emotions']
        self.threshold = self.config.get('classification_threshold', 0.3)
        
        print(f"Loading model from: {model_path}")
        self.model = tf.keras.models.load_model(model_path)
        print("Model loaded successfully!")
    
    def predict(self, text):
        prediction = self.model.predict([text], verbose=0)[0]
        
        detected_emotions = []
        for idx, prob in enumerate(prediction):
            if prob > self.threshold:
                detected_emotions.append({
                    'emotion': self.emotions[idx],
                    'confidence': float(prob)
                })
        
        detected_emotions.sort(key=lambda x: x['confidence'], reverse=True)
        
        top_emotion_idx = np.argmax(prediction)
        top_emotion = self.emotions[top_emotion_idx]
        top_confidence = float(prediction[top_emotion_idx])
        
        return {
            'text': text,
            'top_emotion': top_emotion,
            'top_confidence': top_confidence,
            'detected_emotions': detected_emotions,
            'all_probabilities': {
                self.emotions[i]: float(prediction[i]) 
                for i in range(len(self.emotions))
            }
        }
    
    def get_emotion_response(self, text):
        prediction = self.predict(text)
        top_emotion = prediction['top_emotion']
        
        response_templates = {
            'sadness': {
                'approach': 'empathetic_support',
                'tone': 'gentle and understanding',
                'suggestion': 'Acknowledge feelings, offer comfort, explore coping strategies'
            },
            'anger': {
                'approach': 'calm_validation',
                'tone': 'calm and validating',
                'suggestion': 'Validate feelings, explore triggers, discuss healthy expression'
            },
            'fear': {
                'approach': 'reassuring_support',
                'tone': 'calm and reassuring',
                'suggestion': 'Provide safety, explore fears, discuss coping mechanisms'
            },
            'nervousness': {
                'approach': 'grounding_support',
                'tone': 'calm and grounding',
                'suggestion': 'Offer grounding techniques, validate concerns, explore solutions'
            },
            'joy': {
                'approach': 'positive_reinforcement',
                'tone': 'warm and encouraging',
                'suggestion': 'Celebrate positive moments, reinforce healthy behaviors'
            },
            'gratitude': {
                'approach': 'positive_reinforcement',
                'tone': 'warm and supportive',
                'suggestion': 'Encourage gratitude practice, build on positive momentum'
            },
            'grief': {
                'approach': 'compassionate_presence',
                'tone': 'gentle and compassionate',
                'suggestion': 'Provide space for feelings, offer comfort, discuss healing'
            },
            'confusion': {
                'approach': 'clarifying_support',
                'tone': 'patient and clarifying',
                'suggestion': 'Help organize thoughts, explore situation, provide guidance'
            },
            'disappointment': {
                'approach': 'validating_support',
                'tone': 'understanding and supportive',
                'suggestion': 'Validate disappointment, explore expectations, find perspective'
            },
            'neutral': {
                'approach': 'open_exploration',
                'tone': 'open and curious',
                'suggestion': 'Explore current state, check in on wellbeing, offer support'
            }
        }
        
        response = response_templates.get(top_emotion, response_templates['neutral'])
        
        return {
            **prediction,
            'response_approach': response['approach'],
            'suggested_tone': response['tone'],
            'coaching_suggestion': response['suggestion']
        }


@app.route('/api/predict', methods=['POST'])
def predict():
    """Predict emotion from text"""
    try:
        data = request.json
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        result = predictor.get_emotion_response(text)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/predict/batch', methods=['POST'])
def predict_batch():
    """Predict emotions for multiple texts"""
    try:
        data = request.json
        texts = data.get('texts', [])
        
        if not texts or not isinstance(texts, list):
            return jsonify({'error': 'Invalid input. Provide array of texts'}), 400
        
        results = []
        for text in texts:
            result = predictor.get_emotion_response(text)
            results.append(result)
        
        return jsonify({'predictions': results})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': predictor is not None,
        'tensorflow_version': tf.__version__
    })


@app.route('/api/emotions', methods=['GET'])
def get_emotions():
    """Get list of all emotions"""
    return jsonify({
        'emotions': predictor.emotions,
        'count': len(predictor.emotions)
    })


@app.route('/api/info', methods=['GET'])
def get_info():
    """Get model information"""
    return jsonify({
        'emotions': predictor.emotions,
        'num_emotions': predictor.num_emotions,
        'threshold': predictor.threshold,
        'model_config': predictor.config
    })


def initialize_predictor(model_path, config_path):
    """Initialize the global predictor"""
    global predictor
    predictor = EmotionPredictor(model_path, config_path)


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python api_server.py <model_path> <config_path>")
        print("\nExample:")
        print("python api_server.py trained_models/emotion_bert_20231229_120000/final_model trained_models/emotion_bert_20231229_120000/config.json")
        sys.exit(1)
    
    model_path = sys.argv[1]
    config_path = sys.argv[2]
    
    # Initialize predictor
    initialize_predictor(model_path, config_path)
    
    print("\n" + "="*70)
    print("Starting Emotion Detection API Server")
    print("="*70)
    print(f"\nModel: {model_path}")
    print(f"Config: {config_path}")
    print(f"\nAPI Endpoints:")
    print("  POST   /api/predict       - Predict emotion from text")
    print("  POST   /api/predict/batch - Predict emotions for multiple texts")
    print("  GET    /api/health        - Health check")
    print("  GET    /api/emotions      - Get all emotions")
    print("  GET    /api/info          - Get model info")
    print(f"\nServer running on: http://localhost:5000")
    print("="*70 + "\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
