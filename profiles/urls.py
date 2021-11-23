from django.urls import path

from .views import (
    profileView,
    friend_requests_view,
    # accepted_friends_view,
    profile_list_view,
    suggested_friends_view
)
app_name = 'profiles'
urlpatterns = [
    path('all-friends/', profile_list_view, name='all-friends'),
    path('friend-requests/', friend_requests_view, name='friend-requests'),
    # path('accepted-friends/', accepted_friends_view, name='accepted-friends'),
    path('suggested-friends/', suggested_friends_view, name='suggested-friends'),
    path('<str:pk>/', profileView, name='user-profile'),
]