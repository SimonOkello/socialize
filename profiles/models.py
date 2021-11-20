from django.db import models
from django.contrib.auth.models import User
from django.dispatch.dispatcher import receiver
from django.template.defaultfilters import slugify
# Create your models here.

from .utils import generate_random_code


class Profile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    bio = models.TextField(default='No bio yet', max_length=300)
    email = models.EmailField(max_length=200, blank=True)
    country = models.CharField(max_length=200, blank=True)
    avatar = models.ImageField(upload_to='avatars', default='avatar.png')
    friends = models.ManyToManyField(
        to=User, blank=True, related_name='friends')
    slug = models.SlugField(unique=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_all_friends(self):
        return self.friends.all()

    def get_number_of_friends(self):
        return self.friends.all().count()

    def get_number_of_posts(self):
        return self.posts.all().count()

    def get_all_author_posts(self):
        return self.posts.all()

    def get_number_of_likes_given(self):
        likes = self.like_set.all()
        total_likes = 0
        for item in likes:
            if item.value == 'Like':
                total_likes += 1

        return total_likes

    def get_number_of_likes_received(self):
        posts = self.posts.all()
        total_likes_received = 0
        for item in posts:
            total_likes_received += item.liked.all().count()

        return total_likes_received

    def __str__(self):
        return str(self.user.username)

    def save(self, *args, **kwargs):
        ex = False
        if self.first_name and self.last_name:
            to_slug = slugify(str(self.first_name) + " " + str(self.last_name))
            ex = Profile.objects.filter(slug=to_slug).exists()
            while ex:
                to_slug = slugify(to_slug+" "+str(generate_random_code()))
                ex = Profile.objects.filter(slug=to_slug).exists()
        else:
            to_slug = str(self.user)
        self.slug = to_slug
        super().save(*args, **kwargs)


STATUS_CHOICE = (
    ('Send', 'Send'),
    ('Accepted', 'Accepted'),
)


class RelationshipManager(models.Manager):
    def friend_requests(self, receiver):
        qs = Relationship.objects.filter(receiver=receiver, status='Send')
        return qs


class Relationship(models.Model):
    sender = models.ForeignKey(
        to=Profile, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(
        to=Profile, on_delete=models.CASCADE, related_name='receiver')
    status = models.CharField(max_length=8, choices=STATUS_CHOICE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = RelationshipManager()

    def __str__(self):
        return f"{self.sender}-{self.receiver}-{self.status}"
