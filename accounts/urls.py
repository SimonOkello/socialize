from django.urls import path

from .views import (
    registerView,
    loginView,
    userLogOut

)
app_name = 'accounts'
urlpatterns = [
    path('register/', registerView, name='register'),
    path('login/', loginView, name='login'),
    path('logout/', userLogOut, name='logout'),
    ]