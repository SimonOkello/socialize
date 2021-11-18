from django import forms
from django.db.models import fields
from django.forms import widgets
from .models import Profile


class ProfileModelForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'country', 'bio', 'avatar', ]

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'input'}),
            'last_name': forms.TextInput(attrs={'class': 'input'}),
            'country': forms.TextInput(attrs={'class': 'input'}),
            'bio': forms.Textarea(attrs={'class': 'textarea', 'rows':5}),
            'first_name': forms.TextInput(attrs={'class': 'input'}),
        }
