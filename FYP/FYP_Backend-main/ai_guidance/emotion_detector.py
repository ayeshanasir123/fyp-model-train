"""
Emotion Detection Service for Django Backend
Uses the emotion detection from mock_api_server.py (yesterday's work)
"""

import sys
import os

# Add the parent directory to Python path to import from model training folder
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'model training'))

from typing import Dict, List

class EmotionDetector:
    """
    Lightweight emotion detector using keyword matching
    Can be upgraded to BERT model later
    """
    
    def __init__(self):
        # 28 emotions from GoEmotions dataset
        self.emotions = [
            'admiration', 'amusement', 'anger', 'annoyance', 'approval',
            'caring', 'confusion', 'curiosity', 'desire', 'disappointment',
            'disapproval', 'disgust', 'embarrassment', 'excitement', 'fear',
            'gratitude', 'grief', 'joy', 'love', 'nervousness',
            'optimism', 'pride', 'realization', 'relief', 'remorse',
            'sadness', 'surprise', 'neutral'
        ]
        
        # Use keyword patterns from mock_api_server.py (yesterday's work)
        self.emotion_keywords = {
            'sadness': [
                r'\b(sad|depressed|down|unhappy|miserable|blue|crying|tears|heartbroken|lonely|empty)\b',
                r'\b(feel (bad|terrible|awful)|can\'t cope)\b'
            ],
            'anger': [
                r'\b(angry|mad|furious|annoyed|frustrated|irritated|rage|hate|pissed)\b',
                r'\b(makes me (angry|mad)|so (angry|mad))\b'
            ],
            'fear': [
                r'\b(scared|afraid|terrified|frightened|fearful|panic|dread)\b',
                r'\b(makes me (nervous|anxious|scared))\b'
            ],
            'nervousness': [
                r'\b(nervous|anxious|stressed|tense|uneasy|worried|restless|on edge)\b',
                r'\b(can\'t relax|feel (nervous|anxious))\b'
            ],
            'joy': [
                r'\b(happy|joyful|thrilled|delighted|cheerful|pleased|content|glad)\b',
                r'\b(feel (great|amazing|wonderful|fantastic))\b'
            ],
            'gratitude': [
                r'\b(grateful|thankful|appreciative|blessed|thank you|thanks)\b',
                r'\b(appreciate|value|grateful for)\b'
            ],
            'grief': [
                r'\b(grief|loss|mourning|heartbroken|bereaved|devastated)\b',
                r'\b(lost (someone|my)|passed away)\b'
            ],
            'confusion': [
                r'\b(confused|puzzled|uncertain|unclear|lost|don\'t (know|understand))\b',
                r'\b(not sure|no idea|can\'t figure)\b'
            ],
            'disappointment': [
                r'\b(disappointed|let down|discouraged|disillusioned|failed)\b',
                r'\b(expected (more|better)|didn\'t work out)\b'
            ],
            'love': [
                r'\b(love|adore|cherish|care about|devoted)\b',
                r'\b(in love|love (you|him|her|them))\b'
            ],
            'excitement': [
                r'\b(excited|thrilled|pumped|enthusiastic|eager|looking forward)\b',
                r'\b(can\'t wait|so excited)\b'
            ],
            'caring': [
                r'\b(care|concerned|worry about|hope (you|they))\b',
                r'\b(take care|look after|support)\b'
            ],
            'approval': [
                r'\b(approve|agree|right|correct|good idea|well done)\b',
                r'\b(makes sense|I (approve|agree))\b'
            ],
            'curiosity': [
                r'\b(curious|wonder|interested|intrigued)\b',
                r'\b(want to know|tell me more|how (does|do))\b'
            ],
            'disgust': [
                r'\b(disgusted|revolted|repulsed|gross|sick|nasty)\b',
                r'\b(makes me (sick|disgusted))\b'
            ],
            'embarrassment': [
                r'\b(embarrassed|ashamed|humiliated|awkward)\b',
                r'\b(feel (embarrassed|ashamed))\b'
            ],
            'optimism': [
                r'\b(optimistic|hopeful|positive|bright|better)\b',
                r'\b(things will|going to be (better|good))\b'
            ],
            'pride': [
                r'\b(proud|accomplished|achievement|success)\b',
                r'\b(proud of|feel proud)\b'
            ],
            'relief': [
                r'\b(relief|relieved|glad it\'s over|finally)\b',
                r'\b(feel (relieved|better now))\b'
            ],
            'remorse': [
                r'\b(sorry|regret|guilt|ashamed|shouldn\'t have)\b',
                r'\b(feel (guilty|bad about))\b'
            ],
            'surprise': [
                r'\b(surprised|shocked|amazed|astonished|unexpected|wow)\b',
                r'\b(didn\'t expect|never thought)\b'
            ],
            'annoyance': [
                r'\b(annoyed|bothered|irritated|frustrated|bugged)\b',
                r'\b(getting on my nerves|so annoying)\b'
            ],
            'disapproval': [
                r'\b(disapprove|disagree|wrong|shouldn\'t|bad idea)\b',
                r'\b(don\'t (like|approve)|not right)\b'
            ],
            'desire': [
                r'\b(want|wish|desire|crave|need|long for)\b',
                r'\b(really want|would love)\b'
            ],
            'realization': [
                r'\b(realize|understand now|figured out|makes sense|see now)\b',
                r'\b(I (get it|understand))\b'
            ]
        }
        
        # Response coaching templates
        self.coaching_templates = {
            'sadness': {
                'approach': 'empathetic_support',
                'tone': 'gentle and understanding',
                'prompt_addition': 'The user is expressing sadness. Respond with empathy and understanding. Acknowledge their feelings and gently explore what might help.'
            },
            'anger': {
                'approach': 'calm_validation',
                'tone': 'calm and validating',
                'prompt_addition': 'The user is expressing anger. Validate their feelings calmly. Help them explore the source and healthier ways to express it.'
            },
            'fear': {
                'approach': 'reassuring_support',
                'tone': 'calm and reassuring',
                'prompt_addition': 'The user is expressing fear. Provide calm reassurance. Help them feel safe and explore what they\'re afraid of.'
            },
            'nervousness': {
                'approach': 'grounding_support',
                'tone': 'calm and grounding',
                'prompt_addition': 'The user is expressing anxiety/nervousness. Offer grounding techniques and validate their concerns while exploring solutions.'
            },
            'joy': {
                'approach': 'positive_reinforcement',
                'tone': 'warm and encouraging',
                'prompt_addition': 'The user is expressing joy. Celebrate with them and reinforce this positive moment.'
            },
            'gratitude': {
                'approach': 'positive_reinforcement',
                'tone': 'warm and supportive',
                'prompt_addition': 'The user is expressing gratitude. Acknowledge their appreciation and encourage this positive practice.'
            },
            'grief': {
                'approach': 'compassionate_presence',
                'tone': 'gentle and compassionate',
                'prompt_addition': 'The user is experiencing grief. Provide compassionate presence and space for their feelings. Offer gentle comfort.'
            },
            'confusion': {
                'approach': 'clarifying_support',
                'tone': 'patient and clarifying',
                'prompt_addition': 'The user is confused. Help them organize their thoughts patiently and explore the situation together.'
            },
            'disappointment': {
                'approach': 'validating_support',
                'tone': 'understanding and supportive',
                'prompt_addition': 'The user is disappointed. Validate their feelings and help them explore expectations and find perspective.'
            },
            'neutral': {
                'approach': 'open_exploration',
                'tone': 'open and curious',
                'prompt_addition': 'The user\'s emotion is unclear. Explore their current state with open curiosity and check in on their wellbeing.'
            }
        }
    
    def detect_emotion(self, text: str) -> Dict:
        """
        Detect emotion from text using keyword patterns
        
        Args:
            text: User's message text
            
        Returns:
            Dictionary with emotion, confidence, intensity, and coaching guidance
        """
        text_lower = text.lower()
        emotion_scores = {}
        
        # Score each emotion based on keyword matches
        for emotion, patterns in self.emotion_patterns.items():
            score = 0
            for pattern in patterns:
                matches = re.findall(pattern, text_lower, re.IGNORECASE)
                score += len(matches)
            
            if score > 0:
                emotion_scores[emotion] = score
        
        # Determine top emotion
        if emotion_scores:
            top_emotion = max(emotion_scores, key=emotion_scores.get)
            max_score = emotion_scores[top_emotion]
            
            # Calculate confidence (65-95% range)
            confidence = min(0.65 + (max_score * 0.15), 0.95)
            
            # Calculate intensity (1-10 scale for database)
            intensity = min(int(confidence * 10), 10)
        else:
            top_emotion = 'neutral'
            confidence = 0.70
            intensity = 7
        
        # Get coaching guidance
        coaching = self.coaching_templates.get(
            top_emotion, 
            self.coaching_templates['neutral']
        )
        
        # Get other detected emotions
        other_emotions = [
            {'emotion': e, 'score': s} 
            for e, s in sorted(emotion_scores.items(), key=lambda x: x[1], reverse=True)
            if e != top_emotion
        ][:3]  # Top 3 other emotions
        
        return {
            'emotion': top_emotion,
            'confidence': round(confidence, 3),
            'intensity': intensity,
            'approach': coaching['approach'],
            'tone': coaching['tone'],
            'prompt_addition': coaching['prompt_addition'],
            'other_emotions': other_emotions,
            'all_scores': emotion_scores
        }
    
    def get_emotion_id_from_name(self, emotion_name: str) -> str:
        """
        Get emotion ID/name for database storage
        Normalizes emotion name to match database
        """
        return emotion_name.lower().strip()
    
    def enhance_prompt_with_emotion(self, user_message: str, emotion_data: Dict) -> str:
        """
        Enhance the AI prompt with emotion context
        
        Args:
            user_message: Original user message
            emotion_data: Detected emotion data
            
        Returns:
            Enhanced message with emotion context for better AI response
        """
        emotion_context = emotion_data['prompt_addition']
        
        enhanced_prompt = f"""Context: {emotion_context}

User's message: {user_message}

Respond appropriately with a {emotion_data['tone']} tone, using the {emotion_data['approach']} approach."""
        
        return enhanced_prompt


# Singleton instance
_emotion_detector = None

def get_emotion_detector() -> EmotionDetector:
    """Get or create emotion detector singleton"""
    global _emotion_detector
    if _emotion_detector is None:
        _emotion_detector = EmotionDetector()
    return _emotion_detector
