# users/serializers.py
from rest_framework import serializers
from .models import UserProfile, Skill
from django.contrib.auth.models import User

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name']

class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    skills_offered = SkillSerializer(many=True)
    skills_sought = SkillSerializer(many=True)
    user_id = serializers.ReadOnlyField(source='user.id')  # Add this line

    class Meta:
        model = UserProfile
        fields = ['user', 'user_id', 'location', 'bio', 'skills_offered', 'skills_sought']
