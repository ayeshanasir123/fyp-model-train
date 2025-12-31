from rest_framework import serializers
from .models import ai_guidance

class AIGuidanceSerializer(serializers.ModelSerializer):
    # Add these fields to show emotion details in the response
    emotion_name = serializers.SerializerMethodField()
    emotion_intensity = serializers.SerializerMethodField()
    
    class Meta:
        model = ai_guidance
        fields = [
            'guidance_id', 
            'emotion_id', 
            'emotion_name',      # NEW: emotion name
            'emotion_intensity',  # NEW: emotion intensity
            'suggestion', 
            'effectiveness', 
            'user_message',
            'ai_response',
            'created_at'
        ]
        read_only_fields = ('guidance_id', 'created_at')

    def get_emotion_name(self, obj):
        """Get the emotion name from the related emotion_data"""
        if obj.emotion_id:
            return obj.emotion_id.emotion
        return None
    
    def get_emotion_intensity(self, obj):
        """Get the emotion intensity from the related emotion_data"""
        if obj.emotion_id:
            return obj.emotion_id.intensity
        return None