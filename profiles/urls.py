from django.urls import path

from .views import (
    profileView,
    friend_requests_view,
    # accepted_friends_view,
    profile_list_view,
    suggested_friends_view,
    sendRequestView,
    removeFriendView,
    accept_friend_request,
    reject_friend_request,
)
app_name = 'profiles'
urlpatterns = [
    path('all-friends/', profile_list_view, name='all-friends'),
    path('send-request/', sendRequestView, name='send-request'),
    path('remove-friend/', removeFriendView, name='remove-friend'),
    path('friend-requests/', friend_requests_view, name='friend-requests'),
    # path('accepted-friends/', accepted_friends_view, name='accepted-friends'),
    path('accept-request/', accept_friend_request, name='accept-request'),
    path('reject-request/', reject_friend_request, name='reject-request'),
    path('suggested-friends/', suggested_friends_view, name='suggested-friends'),
    path('<str:pk>/', profileView, name='user-profile'),
]
