from django.urls import path
from .views import ProfileUpdate
from accounts.views import ProfileDetailView, profile_unfollow, profile_follow

app_name = 'accounts'

urlpatterns = [
    path('profile/<str:username>/', ProfileDetailView.as_view(), name='profile'),
    path('follow/<str:username>/', profile_follow, name='profile_follow'),
    path('unfollow/<str:username>/', profile_unfollow, name='profile_unfollow'),
    path('profile/update/<int:pk>', ProfileUpdate.as_view(), name='profile_update'),
]
