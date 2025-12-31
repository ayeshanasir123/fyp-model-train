# HUMAN_COACH/serializers.py
from rest_framework import serializers
from .models import human_coach

class HumanCoachSerializer(serializers.ModelSerializer):
    class Meta:
        model = human_coach
        fields = ('coach_id', 'user_id', 'full_name', 'specialization')
        read_only_fields = ('coach_id',)