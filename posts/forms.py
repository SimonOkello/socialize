from django import forms
from django.db.models import fields
from django.forms import widgets

from posts.models import Post
from .models import Post, Comment


class CreatePostModelForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image']

        widgets = {
            'content': forms.Textarea(attrs={'class': 'textarea', 'rows': 3, 'placeholder': 'Create a Post'})
        }


class CommentModelForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body',]

        widgets = {
            'body': forms.TextInput(attrs={'class': 'input is-normal', 'placeholder': 'Comment here ...'})
        }
