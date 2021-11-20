from django.shortcuts import redirect, render
from django.contrib.auth import logout, login, authenticate

# Create your views here.

def userLogOut(request):
    logout(request)
    return redirect('posts:post-list-view')