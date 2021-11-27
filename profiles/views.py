from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from .models import Profile, Relationship, RelationshipManager
from .forms import ProfileModelForm
from django.contrib.auth.models import User
from django.db.models import Q

# Create your views here.


def profileView(request, pk):
    obj = Profile.objects.get(pk=pk)
    _friend_req_receivers = Relationship.objects.filter(sender=obj)
    _friend_req_senders = Relationship.objects.filter(receiver=obj)
    requests_receivers = []
    requests_senders = []
    for item in _friend_req_receivers:
        requests_receivers.append(item.receiver.user)
    for item in _friend_req_senders:
        requests_senders.append(item.sender.user)
    print('OBJ:', obj)
    print('RECEIV:', requests_receivers)
    print('SENDERS:', requests_senders)
    form = ProfileModelForm(instance=obj)
    if request.method == 'POST':
        form = ProfileModelForm(request.POST or None,
                                request.FILES or None, instance=obj)
        if form.is_valid():
            form.save()
    context = {'obj': obj, 'requests_receivers': requests_receivers,
               'requests_senders': requests_senders, 'form': form}
    return render(request, 'profiles/profile.html', context)


def friend_requests_view(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    qs = Relationship.objects.friend_requests(profile)
    context = {'qs': qs}
    return render(request, 'profiles/friend-requests.html', context)


def accept_friend_request(request):
    if request.method == 'POST' and 'acceptBtn' in request.POST:
        try:
            pk = request.POST.get('profile_pk')
            user = request.user
            sender = Profile.objects.get(pk=pk)
            receiver = Profile.objects.get(user=user)
            relationship = get_object_or_404(
                Relationship, sender=sender, receiver=receiver)
            if relationship.status == 'Send':
                relationship.status = 'Accepted'
                relationship.save()
                sender.friends.add(receiver.user)
                receiver.friends.add(sender.user)
                return redirect('profiles:friend-requests')
        except Profile.DoesNotExist:
            messages.error(request, "Profile does not exist")
            return redirect('profiles:friend-requests')

    return redirect('profiles:friend-requests')


def reject_friend_request(request):
    if request.method == 'POST' and 'rejectBtn' in request.POST:
        try:
            pk = request.POST.get('profile_pk')
            print("PK:", pk)
            user = request.user
            sender = Profile.objects.get(pk=pk)
            receiver = Profile.objects.get(user=user)
            relationship = get_object_or_404(
                Relationship, sender=sender, receiver=receiver)
            relationship.delete()
            return redirect('profiles:friend-requests')
        except Profile.DoesNotExist:
            messages.error(request, "Profile does not exist")
            return redirect('profiles:friend-requests')

    return redirect('profiles:friend-requests')


# def accepted_friends_view(request):
#     user = request.user
#     profile = Profile.objects.get(user=user)
#     my_friends = Relationship.objects.accepted_friends(profile)
#     context = {'my_friends': my_friends}
#     return render(request, 'profiles/friend-requests.html', context)


def profile_list_view(request):
    user = User.objects.get(username=request.user)
    qs = Profile.objects.get_all_profiles(user)
    profile = Profile.objects.get(user=user)
    _friend_req_receivers = Relationship.objects.filter(sender=profile)
    _friend_req_senders = Relationship.objects.filter(receiver=profile)
    requests_receivers = []
    requests_senders = []
    for item in _friend_req_receivers:
        requests_receivers.append(item.receiver.user)
    for item in _friend_req_senders:
        requests_senders.append(item.sender.user)
    context = {'user': user, 'qs': qs, 'requests_receivers': requests_receivers,
               'requests_senders': requests_senders}
    return render(request, 'profiles/all-friends.html', context)


def suggested_friends_view(request):
    user = request.user
    qs = Profile.objects.get_all_available_profiles_to_request(user)
    context = {'qs': qs}
    return render(request, 'profiles/suggested-friends.html', context)


def sendRequestView(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)
        relationship = Relationship.objects.create(
            sender=sender, receiver=receiver, status='Send')

        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles:user-profile')


def removeFriendView(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)
        relationship = Relationship.objects.get(
            (Q(sender=sender) & Q(receiver=receiver)) | (
                Q(sender=receiver) & Q(receiver=sender)))
        relationship.delete()

        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles:user-profile')
