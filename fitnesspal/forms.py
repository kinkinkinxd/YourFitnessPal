"""Forms class for user and profile update form."""
from django import forms
from django.contrib.auth.models import User
from .models import Profile
from django.contrib import messages


class UserUpdateForm(forms.ModelForm):
    """Class for users basic info form update."""

    class Meta:
        """Class for user's firstname, lastname, and email."""

        model = User
        fields = ['first_name', 'last_name', 'email']


class ProfileUpdateForm(forms.ModelForm):
    """Class for users physicality info form update."""

    class Meta:
        """Class for user's physicality info."""

        model = Profile
        fields = ('gender', 'weight', 'height', 'age', 'goal')