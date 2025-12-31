from rest_framework import serializers
from .models import emotion_data

class EmotionDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = emotion_data
        fields = '__all__' # This includes emotion_id, client_id, session_id, emotion, and intensity