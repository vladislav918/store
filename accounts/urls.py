from django.urls import path
from .views import ProfileUpdate
from . import views


app_name = 'accounts'

urlpatterns = [
    path('profile/<str:username>/', views.profile, name='profile'),
    path('profile/<str:username>/follow/', views.profile_follow, name='profile_follow'),
    path('profile/<str:username>/unfollow/', views.profile_unfollow, name='profile_unfollow'),
    path('profile/update/<int:pk>', ProfileUpdate.as_view(), name='profile_update'),
]
