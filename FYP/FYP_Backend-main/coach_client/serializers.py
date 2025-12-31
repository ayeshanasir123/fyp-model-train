# COACH_CLIENT/serializers.py
from rest_framework import serializers
from .models import coach_client

class CoachClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = coach_client
        fields = ('coach_client_id', 'coach_id', 'client_id', 'assigned_date', 'status')
        read_only_fields = ('coach_client_id',)