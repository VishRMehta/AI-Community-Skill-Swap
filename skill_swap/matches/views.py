# matches/views.py
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from users.models import UserProfile  # Import UserProfile
from .algorithm import find_best_matches
from users.serializers import UserProfileSerializer

import logging

logger = logging.getLogger(__name__)

class MatchmakingView(APIView):
    def get(self, request, user_id, format=None):
        try:
            logger.info(f"MatchmakingView: Received request for user_id: {user_id}")
            
            best_match_ids = find_best_matches(user_id)

            logger.info(f"MatchmakingView: Best matches for user_id {user_id}: {best_match_ids}")

            if not best_match_ids:
                return Response([], status=200)
            
            matched_profiles = UserProfile.objects.filter(user__id__in=best_match_ids)
            logger.info(f"MatchmakingView: Matched profiles: {matched_profiles}")

            serializer = UserProfileSerializer(matched_profiles, many=True)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"MatchmakingView: Exception occurred - {str(e)}", exc_info=True)
            return Response({"error": str(e)}, status=400)
