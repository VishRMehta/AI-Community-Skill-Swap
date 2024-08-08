# matches/views.py
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from users.models import UserProfile  # Import UserProfile
from .algorithm import find_best_matches
from users.serializers import UserProfileSerializer

class MatchmakingView(APIView):
    def get(self, request, user_id, format=None):
        try:
            best_match_ids = find_best_matches(user_id)
            if not best_match_ids:
                return Response([], status=200)
            
            # Query UserProfile objects instead of User
            matched_profiles = UserProfile.objects.filter(user__id__in=best_match_ids)
            
            serializer = UserProfileSerializer(matched_profiles, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=400)
