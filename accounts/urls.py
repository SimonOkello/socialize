from django.urls import path

from .views import (
    userLogOut,
)
app_name = 'accounts'
urlpatterns = [
    path('logout/', userLogOut, name='log-out'),
    ]