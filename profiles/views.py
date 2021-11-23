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


# def accepted_friends_view(request):
#     user = request.user
#     profile = Profile.objects.get(user=user)
#     my_friends = Relationship.objects.accepted_friends(profile)
#     context = {'my_friends': my_friends}
#     return render(request, 'profiles/friend-requests.html', context)


def profile_list_view(request):
    user = request.user
    qs = Profile.objects.get_all_profiles(user)
    context = {'qs': qs}
    return render(request, 'profiles/all-friends.html', context)


def suggested_friends_view(request):
    user = request.user
    qs = Profile.objects.get_all_available_profiles_to_request(user)
    context = {'qs': qs}
    return render(request, 'profiles/suggested-friends.html', context)
