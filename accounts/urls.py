from django.urls import path
from .views import ProfileUpdate
from accounts.views import ProfileDetailView, profile_unfollow, profile_follow, send_email_user

app_name = 'accounts'

urlpatterns = [
    path('profile/<str:username>/', ProfileDetailView.as_view(), name='profile'),
    path('follow/<str:username>/', profile_follow, name='profile_follow'),
    path('send_email', send_email_user, name='send_email_user'),
    path('unfollow/<str:username>/', profile_unfollow, name='profile_unfollow'),
    path('profile/update/<int:pk>', ProfileUpdate.as_view(), name='profile_update'),
]
