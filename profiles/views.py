from django.shortcuts import get_object_or_404, render
from .models import Profile
from .forms import ProfileModelForm

# Create your views here.
def profileView(request, pk):
    user = request.user
    obj= Profile.objects.get(user=user)
    form = ProfileModelForm(instance=obj)
    if request.method =='POST':
        form = ProfileModelForm(request.POST or None, request.FILES or None, instance=obj)
        if form.is_valid():
            form.save()
    context = {'obj':obj, 'form':form}
    return render(request, 'profiles/profile.html', context)