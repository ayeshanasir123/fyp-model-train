# NOTIFICATION/serializers.py
from rest_framework import serializers
from .models import notification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = notification
        fields = ('notification_id', 'user_id', 'message', 'date')
        read_only_fields = ('notification_id', 'date')