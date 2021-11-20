from django.shortcuts import get_object_or_404, render
from .models import Profile, Relationship, RelationshipManager
from .forms import ProfileModelForm

# Create your views here.


def profileView(request, pk):
    user = request.user
    obj = Profile.objects.get(user=user)
    form = ProfileModelForm(instance=obj)
    if request.method == 'POST':
        form = ProfileModelForm(request.POST or None,
                                request.FILES or None, instance=obj)
        if form.is_valid():
            form.save()
    context = {'obj': obj, 'form': form}
    return render(request, 'profiles/profile.html', context)


def friend_requests_view(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    qs = Relationship.objects.friend_requests(profile)
    print('FRIENDS:', qs)
    context = {'qs': qs}
    return render(request, 'profiles/friend-requests.html', context)
