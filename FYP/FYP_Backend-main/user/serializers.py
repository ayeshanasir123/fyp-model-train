# USER/serializers.py
from rest_framework import serializers
from .models import user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = user
        fields = ('user_id', 'name', 'email', 'role', 'created_at')
        # user_id and created_at are usually read-only
        read_only_fields = ('user_id', 'created_at')