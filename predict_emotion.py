"""
Inference script for emotion detection - for integration with React frontend
"""

import os
import json
import numpy as np
import tensorflow as tf


class EmotionPredictor:
    """Real-time emotion prediction for mental health coaching"""
    
    def __init__(self, model_path, config_path):
        """
        Initialize predictor
        
        Args:
            model_path: Path to saved model directory
            config_path: Path to config.json file
        """
        # Load configuration
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        self.emotions = self.config['emotions']
        self.num_emotions = self.config['num_emotions']
        self.threshold = self.config.get('classification_threshold', 0.3)
        
        # Load model
        print(f"Loading model from: {model_path}")
        self.model = tf.keras.models.load_model(model_path)
        print("Model loaded successfully!")
    
    def predict(self, text):
        """
        Predict emotions from text
        
        Args:
            text: Input text string
            
        Returns:
            Dictionary with detected emotions and probabilities
        """
        # Make prediction
        prediction = self.model.predict([text], verbose=0)[0]
        
        # Get top emotions above threshold
        detected_emotions = []
        for idx, prob in enumerate(prediction):
            if prob > self.threshold:
                detected_emotions.append({
                    'emotion': self.emotions[idx],
                    'confidence': float(prob)
                })
        
        # Sort by confidence
        detected_emotions.sort(key=lambda x: x['confidence'], reverse=True)
        
        # Get top emotion
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
    
    def predict_batch(self, texts):
        """
        Predict emotions for multiple texts
        
        Args:
            texts: List of text strings
            
        Returns:
            List of prediction dictionaries
        """
        results = []
        for text in texts:
            results.append(self.predict(text))
        return results
    
    def get_emotion_response(self, text):
        """
        Get emotion prediction with appropriate response template
        Useful for mental health coaching context
        
        Args:
            text: Input text from client
            
        Returns:
            Dictionary with emotion and suggested response approach
        """
        prediction = self.predict(text)
        top_emotion = prediction['top_emotion']
        confidence = prediction['top_confidence']
        
        # Response templates based on emotions
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
            'anxiety': {
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
            'neutral': {
                'approach': 'open_exploration',
                'tone': 'open and curious',
                'suggestion': 'Explore current state, check in on wellbeing, offer support'
            }
        }
        
        # Get response approach (default to neutral if emotion not in templates)
        response = response_templates.get(
            top_emotion, 
            response_templates['neutral']
        )
        
        return {
            **prediction,
            'response_approach': response['approach'],
            'suggested_tone': response['tone'],
            'coaching_suggestion': response['suggestion']
        }


def test_predictor(model_path, config_path):
    """Test the predictor with sample texts"""
    
    predictor = EmotionPredictor(model_path, config_path)
    
    # Test samples relevant to mental health coaching
    test_texts = [
        "I've been feeling really down lately and nothing seems to help",
        "I'm so excited about my progress in therapy!",
        "I don't know what to do, everything feels overwhelming",
        "Thank you for always being there to listen",
        "I'm scared about what the future holds",
        "I'm really angry about what happened today",
        "Things are going okay, just the usual"
    ]
    
    print("\n" + "="*70)
    print("Testing Emotion Predictor")
    print("="*70 + "\n")
    
    for text in test_texts:
        result = predictor.get_emotion_response(text)
        
        print(f"Text: {text}")
        print(f"Top Emotion: {result['top_emotion']} (confidence: {result['top_confidence']:.3f})")
        print(f"Approach: {result['response_approach']}")
        print(f"Suggested Tone: {result['suggested_tone']}")
        print(f"Coaching Tip: {result['coaching_suggestion']}")
        
        if result['detected_emotions']:
            print(f"Other detected emotions: {', '.join([f\"{e['emotion']} ({e['confidence']:.3f})\" for e in result['detected_emotions'][:3]])}")
        
        print("-" * 70 + "\n")


# Flask API example for backend integration
def create_flask_api():
    """
    Example Flask API for integration with React frontend
    Save this as separate file: api_server.py
    """
    
    example_code = '''
from flask import Flask, request, jsonify
from flask_cors import CORS
from predict_emotion import EmotionPredictor
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Initialize predictor
MODEL_PATH = "trained_models/emotion_bert_XXXXXX/final_model"
CONFIG_PATH = "trained_models/emotion_bert_XXXXXX/config.json"
predictor = EmotionPredictor(MODEL_PATH, CONFIG_PATH)

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

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'model_loaded': True})

@app.route('/api/emotions', methods=['GET'])
def get_emotions():
    """Get list of all emotions"""
    return jsonify({'emotions': predictor.emotions})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
'''
    
    return example_code


# FastAPI example (modern alternative)
def create_fastapi_api():
    """
    Example FastAPI for integration with React frontend
    Save this as separate file: api_server_fastapi.py
    """
    
    example_code = '''
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from predict_emotion import EmotionPredictor
import uvicorn

app = FastAPI(title="Emotion Detection API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for your React app URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize predictor
MODEL_PATH = "trained_models/emotion_bert_XXXXXX/final_model"
CONFIG_PATH = "trained_models/emotion_bert_XXXXXX/config.json"
predictor = EmotionPredictor(MODEL_PATH, CONFIG_PATH)

class TextInput(BaseModel):
    text: str

class PredictionResponse(BaseModel):
    text: str
    top_emotion: str
    top_confidence: float
    detected_emotions: list
    response_approach: str
    suggested_tone: str
    coaching_suggestion: str

@app.post("/api/predict", response_model=PredictionResponse)
async def predict(input_data: TextInput):
    """Predict emotion from text"""
    try:
        result = predictor.get_emotion_response(input_data.text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "model_loaded": True}

@app.get("/api/emotions")
async def get_emotions():
    """Get list of all emotions"""
    return {"emotions": predictor.emotions}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''
    
    return example_code


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 2:
        # Test with provided model path
        model_path = sys.argv[1]
        config_path = sys.argv[2]
        test_predictor(model_path, config_path)
    else:
        print("Usage: python predict_emotion.py <model_path> <config_path>")
        print("\nExample:")
        print("python predict_emotion.py trained_models/emotion_bert_20231229_120000/final_model trained_models/emotion_bert_20231229_120000/config.json")
        print("\nOr import EmotionPredictor class in your code:")
        print("from predict_emotion import EmotionPredictor")
        print("predictor = EmotionPredictor(model_path, config_path)")
        print("result = predictor.predict('I am feeling happy today')")
