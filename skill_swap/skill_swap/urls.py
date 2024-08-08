from django.contrib import admin
from django.urls import path, include
from users import views as user_views
from matches.views import MatchmakingView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/profiles/', user_views.UserProfileListCreateView.as_view(), name='profile-list'),
    path('api/profiles/<int:pk>/', user_views.UserProfileDetailView.as_view(), name='profile-detail'),
    path('api/matchmaking/<int:user_id>/', MatchmakingView.as_view(), name='matchmaking'),
]
