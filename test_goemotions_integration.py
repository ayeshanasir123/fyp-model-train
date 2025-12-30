"""
Test GoEmotions BERT Detector with 43k training dataset
Validates integration with all 28 emotions and dataset mappings
"""

import sys
sys.path.insert(0, r"c:\Users\99TECH\Desktop\model training\FYP\FYP_Backend-main")

from ai_guidance.goemotions_bert_detector import get_emotion_detector

def test_goemotions_detector():
    """Test the detector with various emotions"""
    
    detector = get_emotion_detector()
    
    print("=" * 80)
    print("GoEmotions BERT Detector - Trained on 43,410 samples")
    print("28 Emotion Categories + Ekman Mapping + Sentiment Analysis")
    print("=" * 80)
    
    # Test messages representing different emotions
    test_cases = [
        "I'm so proud of what I accomplished today!",
        "This is absolutely hilarious, I can't stop laughing!",
        "I'm really confused about what to do next",
        "Thank you so much for your help, I really appreciate it",
        "I'm terrified about the exam tomorrow",
        "I miss them so much, it hurts",
        "This makes me so angry, I can't believe it",
        "I'm curious about how this works",
        "Wow, I didn't expect that at all!",
        "I feel so embarrassed about what happened",
    ]
    
    for i, message in enumerate(test_cases, 1):
        print(f"\n{'─' * 80}")
        print(f"Test {i}: {message}")
        print('─' * 80)
        
        result = detector.detect_emotion(message)
        
        print(f"Primary Emotion: {result['emotion'].upper()}")
        print(f"Confidence: {result['confidence']:.1%}")
        print(f"Intensity: {result['intensity']}/10")
        print(f"Ekman Category: {result['ekman_category']}")
        print(f"Sentiment: {result['sentiment']}")
        print(f"Coaching Approach: {result['approach']}")
        print(f"Tone: {result['tone']}")
        
        if result['secondary_emotions']:
            print(f"\nSecondary Emotions:")
            for sec in result['secondary_emotions']:
                print(f"  - {sec['emotion']}: {sec['score']} matches")
    
    print(f"\n{'=' * 80}")
    print(f"Dataset Information:")
    print(f"  Training Samples: {detector.dataset_stats['train_samples']:,}")
    print(f"  Dev Samples: {detector.dataset_stats['dev_samples']:,}")
    print(f"  Test Samples: {detector.dataset_stats['test_samples']:,}")
    print(f"  Total Samples: {detector.dataset_stats['total_samples']:,}")
    print(f"  Total Emotions: {len(detector.emotions)}")
    print(f"{'=' * 80}")
    
    # Test enhanced prompt
    print(f"\n{'=' * 80}")
    print("Testing Enhanced Prompt Generation")
    print('=' * 80)
    test_msg = "I'm feeling really anxious about my future"
    result = detector.detect_emotion(test_msg)
    enhanced = detector.enhance_prompt_with_emotion(test_msg, result)
    print(enhanced)
    print('=' * 80)

if __name__ == "__main__":
    test_goemotions_detector()
