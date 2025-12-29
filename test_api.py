"""
Test Client for Mock Emotion Detection API
Demonstrates all API endpoints
"""

import requests
import json
import time

API_BASE_URL = "http://localhost:5000/api"

def print_header(text):
    print("\n" + "="*70)
    print(text)
    print("="*70)

def test_health():
    """Test health endpoint"""
    print_header("1. Health Check")
    
    response = requests.get(f"{API_BASE_URL}/health")
    data = response.json()
    
    print(f"Status: {data['status']}")
    print(f"Mode: {data['mode']}")
    print(f"Model Loaded: {data['model_loaded']}")
    print(f"Message: {data['message']}")

def test_emotions():
    """Test emotions list endpoint"""
    print_header("2. Get All Emotions")
    
    response = requests.get(f"{API_BASE_URL}/emotions")
    data = response.json()
    
    print(f"Total Emotions: {data['count']}")
    print(f"Emotions: {', '.join(data['emotions'][:10])}...")

def test_single_prediction():
    """Test single prediction"""
    print_header("3. Single Emotion Prediction")
    
    test_cases = [
        "I'm feeling really sad and down today",
        "I'm so excited about my new job!",
        "I'm confused about what to do next",
        "Thank you so much for your help",
        "I'm worried and anxious about my exam tomorrow"
    ]
    
    for text in test_cases:
        print(f"\nText: '{text}'")
        
        response = requests.post(
            f"{API_BASE_URL}/predict",
            json={"text": text},
            headers={"Content-Type": "application/json"}
        )
        
        data = response.json()
        
        print(f"  🎯 Emotion: {data['top_emotion']}")
        print(f"  📊 Confidence: {data['top_confidence']*100:.1f}%")
        print(f"  💬 Approach: {data['response_approach']}")
        print(f"  🗣️  Tone: {data['suggested_tone']}")
        
        if len(data['detected_emotions']) > 1:
            other = [f"{e['emotion']} ({e['confidence']:.2f})" 
                    for e in data['detected_emotions'][1:3]]
            print(f"  🔍 Other: {', '.join(other)}")
        
        time.sleep(0.2)

def test_batch_prediction():
    """Test batch prediction"""
    print_header("4. Batch Prediction")
    
    texts = [
        "I love spending time with my family",
        "This situation makes me so angry",
        "I'm grateful for all your support"
    ]
    
    print(f"Predicting {len(texts)} texts...")
    
    response = requests.post(
        f"{API_BASE_URL}/predict/batch",
        json={"texts": texts},
        headers={"Content-Type": "application/json"}
    )
    
    data = response.json()
    
    for i, result in enumerate(data['predictions']):
        print(f"\n{i+1}. '{result['text']}'")
        print(f"   → {result['top_emotion']} ({result['top_confidence']*100:.0f}%)")

def test_mental_health_scenarios():
    """Test mental health coaching scenarios"""
    print_header("5. Mental Health Coaching Scenarios")
    
    scenarios = [
        {
            "client": "I've been feeling really depressed lately",
            "context": "Client expressing depression"
        },
        {
            "client": "I'm so angry at my boss for what he said",
            "context": "Client expressing workplace anger"
        },
        {
            "client": "I don't know what to do, everything is overwhelming",
            "context": "Client expressing confusion and overwhelm"
        },
        {
            "client": "I'm scared about my health diagnosis",
            "context": "Client expressing fear about health"
        }
    ]
    
    for scenario in scenarios:
        print(f"\n📝 Scenario: {scenario['context']}")
        print(f"💬 Client: '{scenario['client']}'")
        
        response = requests.post(
            f"{API_BASE_URL}/predict",
            json={"text": scenario['client']},
            headers={"Content-Type": "application/json"}
        )
        
        data = response.json()
        
        print(f"\n   🎯 Detected Emotion: {data['top_emotion']}")
        print(f"   📊 Confidence: {data['top_confidence']*100:.0f}%")
        print(f"   💡 Coaching Approach: {data['response_approach']}")
        print(f"   🗣️  Suggested Tone: {data['suggested_tone']}")
        print(f"   📋 Suggestion: {data['coaching_suggestion']}")
        
        time.sleep(0.3)

def test_api_info():
    """Test API info endpoint"""
    print_header("6. API Information")
    
    response = requests.get(f"{API_BASE_URL}/info")
    data = response.json()
    
    print(f"Mode: {data['mode']}")
    print(f"Number of Emotions: {data['num_emotions']}")
    print(f"Description: {data['description']}")
    print(f"Message: {data['message']}")

def test_sample_predictions():
    """Test sample predictions endpoint"""
    print_header("7. Sample Test Predictions")
    
    response = requests.get(f"{API_BASE_URL}/test")
    data = response.json()
    
    for pred in data['test_predictions']:
        print(f"\n'{pred['text']}'")
        print(f"  → {pred['emotion']} ({pred['confidence']*100:.0f}%)")

def main():
    print("\n" + "="*70)
    print("🧪 EMOTION DETECTION API - TEST CLIENT")
    print("="*70)
    print("\nTesting all API endpoints with mock data...")
    print("Make sure the mock_api_server.py is running on localhost:5000")
    
    try:
        # Run all tests
        test_health()
        test_emotions()
        test_single_prediction()
        test_batch_prediction()
        test_mental_health_scenarios()
        test_api_info()
        test_sample_predictions()
        
        print("\n" + "="*70)
        print("✅ ALL TESTS COMPLETED SUCCESSFULLY!")
        print("="*70)
        print("\n🎉 Your API is working perfectly!")
        print("📱 Ready to integrate with React frontend")
        print("🔗 API URL: http://localhost:5000")
        print("\n💡 Next Steps:")
        print("   1. Use this API with your React frontend")
        print("   2. Test the emotion detection in your chat interface")
        print("   3. Later, train the real BERT model for better accuracy")
        print("="*70 + "\n")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to API server")
        print("Make sure mock_api_server.py is running:")
        print("  python mock_api_server.py")
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")

if __name__ == "__main__":
    main()
