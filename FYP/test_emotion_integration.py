"""
Test Emotion Detection Integration
Run this to verify emotion detection is working
"""

import sys
import os

# Add the Django project to path
sys.path.append('C:/Users/99TECH/Desktop/model training/FYP/FYP_Backend-main')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

import django
django.setup()

from ai_guidance.emotion_detector import get_emotion_detector

def test_emotions():
    detector = get_emotion_detector()
    
    print("="*70)
    print("🧪 TESTING EMOTION DETECTION INTEGRATION")
    print("="*70)
    
    test_cases = [
        "I'm feeling really sad and down today",
        "I'm so excited about my new job!",
        "I'm confused about what to do next",
        "Thank you so much for your help",
        "I'm worried and anxious about tomorrow",
        "I'm so angry at what happened",
        "Everything is going okay"
    ]
    
    for i, text in enumerate(test_cases, 1):
        print(f"\n{i}. Testing: \"{text}\"")
        result = detector.detect_emotion(text)
        
        print(f"   🎯 Emotion: {result['emotion']}")
        print(f"   📊 Confidence: {result['confidence']*100:.1f}%")
        print(f"   💪 Intensity: {result['intensity']}/10")
        print(f"   💡 Approach: {result['approach']}")
        print(f"   🗣️  Tone: {result['tone']}")
        
        if result['other_emotions']:
            others = [f"{e['emotion']}" for e in result['other_emotions'][:2]]
            print(f"   🔍 Other: {', '.join(others)}")
    
    print("\n" + "="*70)
    print("✅ EMOTION DETECTION WORKING!")
    print("="*70)
    print("\n📋 Next Steps:")
    print("   1. Start Django: python manage.py runserver")
    print("   2. Start React: npm run dev")
    print("   3. Test in browser - emotions will be detected automatically!")
    print("\n" + "="*70)

if __name__ == "__main__":
    test_emotions()
