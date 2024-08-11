from rest_framework import generics
from .models import UserProfile, Skill
from .serializers import UserProfileSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User

@api_view(['POST'])
def register_user(request):
    data = request.data

    try:
        # Create the user
        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password']
        )

        # Create the profile
        profile = UserProfile.objects.create(
            user=user,
            location=data['location'],
            bio=data['bio']
        )

        # Add skills offered
        skills_offered = data['skills_offered'].split(',')
        for skill_name in skills_offered:
            skill, created = Skill.objects.get_or_create(name=skill_name.strip())
            profile.skills_offered.add(skill)

        # Add skills sought
        skills_sought = data['skills_sought'].split(',')
        for skill_name in skills_sought:
            skill, created = Skill.objects.get_or_create(name=skill_name.strip())
            profile.skills_sought.add(skill)

        profile.save()

        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UserProfileListCreateView(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class UserProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
