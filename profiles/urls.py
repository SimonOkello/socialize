from django.urls import path

from .views import (
    profileView,
    friend_requests_view,
)
app_name = 'profiles'
urlpatterns = [
    path('friend-requests/', friend_requests_view, name='friend-requests'),
    path('<str:pk>/', profileView, name='user-profile'),
]