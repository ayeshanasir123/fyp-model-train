"""
Mock API Server for Emotion Detection - No Training Required!
Tests the backend API with mock predictions
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import time

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Mock emotion data
EMOTIONS = [
    'admiration', 'amusement', 'anger', 'annoyance', 'approval',
    'caring', 'confusion', 'curiosity', 'desire', 'disappointment',
    'disapproval', 'disgust', 'embarrassment', 'excitement', 'fear',
    'gratitude', 'grief', 'joy', 'love', 'nervousness',
    'optimism', 'pride', 'realization', 'relief', 'remorse',
    'sadness', 'surprise', 'neutral'
]

# Response templates for mental health coaching
RESPONSE_TEMPLATES = {
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

# Keyword-based emotion detection (simple rule-based for demo)
EMOTION_KEYWORDS = {
    'sadness': ['sad', 'down', 'depressed', 'unhappy', 'miserable', 'blue', 'crying'],
    'anger': ['angry', 'mad', 'furious', 'annoyed', 'frustrated', 'irritated'],
    'fear': ['scared', 'afraid', 'terrified', 'frightened', 'anxious', 'worried'],
    'nervousness': ['nervous', 'anxious', 'stressed', 'tense', 'uneasy', 'worried'],
    'joy': ['happy', 'joyful', 'excited', 'thrilled', 'delighted', 'cheerful'],
    'gratitude': ['grateful', 'thankful', 'appreciative', 'blessed', 'thank you'],
    'grief': ['grief', 'loss', 'mourning', 'heartbroken', 'bereaved'],
    'confusion': ['confused', 'puzzled', 'uncertain', 'unclear', 'lost', 'don\'t know'],
    'disappointment': ['disappointed', 'let down', 'discouraged', 'disillusioned'],
    'love': ['love', 'adore', 'cherish', 'care about'],
    'surprise': ['surprised', 'shocked', 'amazed', 'astonished', 'unexpected'],
    'disgust': ['disgusted', 'revolted', 'repulsed', 'gross'],
}

def detect_emotion_from_text(text):
    """Simple keyword-based emotion detection for demo"""
    text_lower = text.lower()
    
    # Check for keyword matches
    emotion_scores = {}
    for emotion, keywords in EMOTION_KEYWORDS.items():
        score = sum(1 for keyword in keywords if keyword in text_lower)
        if score > 0:
            emotion_scores[emotion] = score
    
    if emotion_scores:
        # Get top emotion
        top_emotion = max(emotion_scores, key=emotion_scores.get)
        confidence = min(0.65 + (emotion_scores[top_emotion] * 0.15), 0.95)
    else:
        # Default to neutral
        top_emotion = 'neutral'
        confidence = 0.70
    
    return top_emotion, confidence, emotion_scores

def generate_mock_prediction(text):
    """Generate realistic mock prediction"""
    time.sleep(0.1)  # Simulate processing time
    
    # Detect emotion from keywords
    top_emotion, top_confidence, emotion_scores = detect_emotion_from_text(text)
    
    # Generate other detected emotions
    detected_emotions = []
    for emotion, score in sorted(emotion_scores.items(), key=lambda x: x[1], reverse=True):
        if emotion != top_emotion:
            conf = min(0.3 + (score * 0.1), top_confidence - 0.1)
            detected_emotions.append({
                'emotion': emotion,
                'confidence': round(conf, 3)
            })
    
    # Add primary emotion
    detected_emotions.insert(0, {
        'emotion': top_emotion,
        'confidence': round(top_confidence, 3)
    })
    
    # Generate all probabilities
    all_probabilities = {}
    for emotion in EMOTIONS:
        if emotion == top_emotion:
            all_probabilities[emotion] = round(top_confidence, 3)
        elif emotion in emotion_scores:
            all_probabilities[emotion] = round(min(0.2 + (emotion_scores[emotion] * 0.08), 0.6), 3)
        else:
            all_probabilities[emotion] = round(random.uniform(0.01, 0.15), 3)
    
    # Get response approach
    response = RESPONSE_TEMPLATES.get(top_emotion, RESPONSE_TEMPLATES['neutral'])
    
    return {
        'text': text,
        'top_emotion': top_emotion,
        'top_confidence': round(top_confidence, 3),
        'detected_emotions': detected_emotions[:5],  # Top 5
        'all_probabilities': all_probabilities,
        'response_approach': response['approach'],
        'suggested_tone': response['tone'],
        'coaching_suggestion': response['suggestion']
    }


@app.route('/api/predict', methods=['POST'])
def predict():
    """Predict emotion from text (MOCK VERSION)"""
    try:
        data = request.json
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        result = generate_mock_prediction(text)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/predict/batch', methods=['POST'])
def predict_batch():
    """Predict emotions for multiple texts (MOCK VERSION)"""
    try:
        data = request.json
        texts = data.get('texts', [])
        
        if not texts or not isinstance(texts, list):
            return jsonify({'error': 'Invalid input. Provide array of texts'}), 400
        
        results = []
        for text in texts:
            result = generate_mock_prediction(text)
            results.append(result)
        
        return jsonify({'predictions': results})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'mode': 'MOCK',
        'model_loaded': True,
        'message': 'Running with mock predictions (no ML model required)'
    })


@app.route('/api/emotions', methods=['GET'])
def get_emotions():
    """Get list of all emotions"""
    return jsonify({
        'emotions': EMOTIONS,
        'count': len(EMOTIONS)
    })


@app.route('/api/info', methods=['GET'])
def get_info():
    """Get API information"""
    return jsonify({
        'mode': 'MOCK',
        'emotions': EMOTIONS,
        'num_emotions': len(EMOTIONS),
        'description': 'Mock emotion detection API - keyword-based rules',
        'message': 'This is a demo version using simple keyword matching. Train the real model for ML-based predictions.'
    })


@app.route('/api/test', methods=['GET'])
def test():
    """Test endpoint with sample predictions"""
    test_texts = [
        "I'm feeling really sad and down today",
        "I'm so excited about my new project!",
        "I'm confused about what to do next",
        "Thank you so much for your help",
        "I'm worried about my exam tomorrow"
    ]
    
    results = []
    for text in test_texts:
        result = generate_mock_prediction(text)
        results.append({
            'text': text,
            'emotion': result['top_emotion'],
            'confidence': result['top_confidence']
        })
    
    return jsonify({
        'test_predictions': results,
        'message': 'Sample predictions using mock model'
    })


if __name__ == '__main__':
    print("\n" + "="*70)
    print("🎭 EMOTION DETECTION MOCK API SERVER")
    print("="*70)
    print("\n⚠️  MOCK MODE - Using keyword-based detection (no ML model)")
    print("✓  Perfect for testing React frontend integration")
    print("✓  No training required - works immediately")
    print("\n📡 API Endpoints:")
    print("  POST   /api/predict       - Predict emotion from text")
    print("  POST   /api/predict/batch - Predict emotions for multiple texts")
    print("  GET    /api/health        - Health check")
    print("  GET    /api/emotions      - Get all emotions")
    print("  GET    /api/info          - Get API info")
    print("  GET    /api/test          - Test with sample predictions")
    print(f"\n🌐 Server running on: http://localhost:5000")
    print("="*70)
    print("\n💡 Test it:")
    print("  curl -X POST http://localhost:5000/api/predict -H 'Content-Type: application/json' -d '{\"text\":\"I am feeling happy\"}'")
    print("\n🎯 Train real model later with: python train_emotion_model.py")
    print("="*70 + "\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
