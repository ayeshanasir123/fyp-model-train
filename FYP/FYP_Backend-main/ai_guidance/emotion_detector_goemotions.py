"""
Emotion Detection Service for Django Backend
Uses the same logic as mock_api_server.py from yesterday's work
Integrates with GoEmotions dataset structure
"""

from typing import Dict, List

class EmotionDetector:
    """
    Emotion detector using keyword matching from yesterday's mock_api_server.py
    Works with GoEmotions 28 emotion categories
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
        
        # Keyword-based emotion detection (from yesterday's mock_api_server.py)
        self.emotion_keywords = {
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
        
        # Response templates from yesterday's work (for mental health coaching)
        self.coaching_templates = {
            'sadness': {
                'approach': 'empathetic_support',
                'tone': 'gentle and understanding',
                'prompt_addition': 'The client is expressing sadness. Use empathetic validation, explore underlying causes, and suggest gentle coping strategies.'
            },
            'anger': {
                'approach': 'calm_validation',
                'tone': 'calm and validating',
                'prompt_addition': 'The client is expressing anger. Validate their feelings, explore triggers, and discuss healthy expression methods.'
            },
            'fear': {
                'approach': 'reassuring_support',
                'tone': 'calm and reassuring',
                'prompt_addition': 'The client is expressing fear. Provide reassurance, explore specific fears, and discuss coping mechanisms.'
            },
            'nervousness': {
                'approach': 'grounding_support',
                'tone': 'calm and grounding',
                'prompt_addition': 'The client is experiencing nervousness/anxiety. Offer grounding techniques and validate their concerns.'
            },
            'joy': {
                'approach': 'positive_reinforcement',
                'tone': 'warm and encouraging',
                'prompt_addition': 'The client is expressing joy. Celebrate their positive moment and reinforce healthy behaviors.'
            },
            'gratitude': {
                'approach': 'positive_reinforcement',
                'tone': 'warm and supportive',
                'prompt_addition': 'The client is expressing gratitude. Encourage this positive practice and build on the momentum.'
            },
            'grief': {
                'approach': 'compassionate_presence',
                'tone': 'gentle and compassionate',
                'prompt_addition': 'The client is experiencing grief. Provide space for their feelings and offer gentle comfort.'
            },
            'confusion': {
                'approach': 'clarifying_support',
                'tone': 'patient and clarifying',
                'prompt_addition': 'The client is confused. Help organize their thoughts and provide gentle guidance.'
            },
            'disappointment': {
                'approach': 'validating_support',
                'tone': 'understanding and supportive',
                'prompt_addition': 'The client is disappointed. Validate their feelings and help find perspective.'
            },
            'neutral': {
                'approach': 'open_exploration',
                'tone': 'open and curious',
                'prompt_addition': 'Explore the client\'s current state with openness and offer appropriate support.'
            }
        }
    
    def detect_emotion(self, text: str) -> Dict:
        """
        Detect emotion from text using keyword matching (from yesterday's mock_api_server.py)
        
        Args:
            text: Input text to analyze
            
        Returns:
            dict with emotion, confidence, intensity, and coaching guidance
        """
        text_lower = text.lower()
        
        # Check for keyword matches (same logic as yesterday)
        emotion_scores = {}
        for emotion, keywords in self.emotion_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                emotion_scores[emotion] = score
        
        # Determine top emotion
        if emotion_scores:
            top_emotion = max(emotion_scores, key=emotion_scores.get)
            max_score = emotion_scores[top_emotion]
            
            # Calculate confidence (65-95% range) - same as yesterday
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
        """Get emotion ID/name for database storage"""
        return emotion_name.lower().strip()
    
    def enhance_prompt_with_emotion(self, user_message: str, emotion_data: Dict) -> str:
        """
        Enhance the AI prompt with emotion context (from yesterday's work)
        
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
