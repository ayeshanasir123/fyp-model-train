"""
Standalone Demo - Emotion Detection (No Server Required)
Shows how the mock emotion detection works
"""

import random
import time

# Emotion data
EMOTIONS = [
    'admiration', 'amusement', 'anger', 'annoyance', 'approval',
    'caring', 'confusion', 'curiosity', 'desire', 'disappointment',
    'disapproval', 'disgust', 'embarrassment', 'excitement', 'fear',
    'gratitude', 'grief', 'joy', 'love', 'nervousness',
    'optimism', 'pride', 'realization', 'relief', 'remorse',
    'sadness', 'surprise', 'neutral'
]

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
    'excitement': ['excited', 'thrilled', 'pumped', 'enthusiastic'],
}

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
}

def detect_emotion(text):
    """Simple keyword-based emotion detection"""
    text_lower = text.lower()
    
    emotion_scores = {}
    for emotion, keywords in EMOTION_KEYWORDS.items():
        score = sum(1 for keyword in keywords if keyword in text_lower)
        if score > 0:
            emotion_scores[emotion] = score
    
    if emotion_scores:
        top_emotion = max(emotion_scores, key=emotion_scores.get)
        confidence = min(0.65 + (emotion_scores[top_emotion] * 0.15), 0.95)
    else:
        top_emotion = 'neutral'
        confidence = 0.70
    
    response = RESPONSE_TEMPLATES.get(top_emotion, {
        'approach': 'open_exploration',
        'tone': 'open and curious',
        'suggestion': 'Explore current state, check in on wellbeing'
    })
    
    return {
        'emotion': top_emotion,
        'confidence': confidence,
        'approach': response['approach'],
        'tone': response['tone'],
        'suggestion': response['suggestion']
    }

def print_header(text):
    print("\n" + "="*70)
    print(text)
    print("="*70)

def demo():
    print_header("🎭 EMOTION DETECTION - STANDALONE DEMO")
    print("\n✓ No server required - works immediately")
    print("✓ Keyword-based detection for quick testing")
    print("✓ Ready for React frontend integration")
    
    # Test cases
    test_cases = [
        {
            "text": "I'm feeling really sad and down today",
            "context": "Client expressing sadness"
        },
        {
            "text": "I'm so excited about my new job!",
            "context": "Client expressing excitement"
        },
        {
            "text": "I'm confused about what to do next",
            "context": "Client expressing confusion"
        },
        {
            "text": "Thank you so much for your help and support",
            "context": "Client expressing gratitude"
        },
        {
            "text": "I'm worried and anxious about my exam tomorrow",
            "context": "Client expressing anxiety"
        },
        {
            "text": "I'm so angry at what happened today",
            "context": "Client expressing anger"
        },
        {
            "text": "I'm scared about my future",
            "context": "Client expressing fear"
        },
        {
            "text": "Everything is going okay",
            "context": "Neutral statement"
        }
    ]
    
    print_header("📝 MENTAL HEALTH COACHING SCENARIOS")
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n{i}. {case['context']}")
        print(f"   💬 Client: \"{case['text']}\"")
        
        result = detect_emotion(case['text'])
        
        print(f"\n   🎯 Detected Emotion: {result['emotion'].upper()}")
        print(f"   📊 Confidence: {result['confidence']*100:.0f}%")
        print(f"   💡 Coaching Approach: {result['approach']}")
        print(f"   🗣️  Suggested Tone: {result['tone']}")
        print(f"   📋 Suggestion: {result['suggestion']}")
        print("   " + "-"*66)
        
        time.sleep(0.3)
    
    print_header("✅ DEMO COMPLETE")
    print("\n🎉 Emotion detection is working!")
    print("\n📱 Integration Options:")
    print("   1. Use mock_api_server.py for REST API (Flask)")
    print("   2. Use this code directly in your Python backend")
    print("   3. Connect with React frontend via API calls")
    
    print("\n🔗 API Endpoints (when server is running):")
    print("   POST   http://localhost:5000/api/predict")
    print("   GET    http://localhost:5000/api/emotions")
    print("   GET    http://localhost:5000/api/health")
    
    print("\n🎯 Next Steps:")
    print("   ✓ Test with your React frontend")
    print("   ✓ Integrate emotion-aware responses")
    print("   ✓ Later: Train BERT model for 90%+ accuracy")
    
    print("\n💻 React Integration Example:")
    print("""
    // In your React component
    const detectEmotion = async (text) => {
      const response = await fetch('http://localhost:5000/api/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text })
      });
      const data = await response.json();
      console.log('Emotion:', data.top_emotion);
      return data;
    };
    """)
    
    print("="*70 + "\n")

if __name__ == "__main__":
    demo()
