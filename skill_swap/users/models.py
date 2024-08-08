from django.contrib.auth.models import User
from django.db import models

class Skill(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=255)
    bio = models.TextField(blank=True)
    skills_offered = models.ManyToManyField(Skill, related_name='offered_by')
    skills_sought = models.ManyToManyField(Skill, related_name='sought_by')
    preferences = models.TextField(blank=True)  # Store user preferences as a JSON string
    past_interactions = models.ManyToManyField(User, related_name='interacted_with', blank=True)

    def __str__(self):
        return self.user.username
