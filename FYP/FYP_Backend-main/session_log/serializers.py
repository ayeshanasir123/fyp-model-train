# SESSION_LOG/serializers.py
from rest_framework import serializers
from .models import session_log

class SessionLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = session_log
        fields = ('session_id', 'user_id', 'client_id', 'date', 'notes', 'summary', 'final_emotion', 'emotion_intensity')
        read_only_fields = ('session_id',)