from django.urls import path

from .views import (
    profileView,
)
app_name = 'profiles'
urlpatterns = [
    path('<str:pk>/', profileView, name='user-profile')
]