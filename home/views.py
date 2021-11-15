from django.shortcuts import render

# Create your views here.
def homeView(request):
    user = request.user
    context = {'user': user}
    return render(request, 'home/home.html', context)