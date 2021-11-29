from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User


# Create your views here.
def registerView(request):
    return render(request, 'accounts/register.html')


def loginView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('posts:post-list-view')
        else:
            messages.error(request, 'Username or Password incorrect')
    return render(request, 'accounts/login.html')


def userLogOut(request):
    logout(request)
    return redirect('posts:post-list-view')
