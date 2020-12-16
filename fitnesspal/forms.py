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

    def clean(self):
        cleaned_data = super(ProfileUpdateForm, self).clean()
        input_gender = cleaned_data.get("gender")
        input_weight = cleaned_data.get("weight")
        input_height = cleaned_data.get("height")
        input_age = cleaned_data.get("age")
        input_goal = cleaned_data.get("goal")
        if input_gender != "Male" and input_gender != "Female":
            raise forms.ValidationError("Please input only Male or Female!")
        if input_weight < 0 or input_height < 0 or input_age < 0 or input_goal < 0:
            raise forms.ValidationError("Please input positive number!")
        return cleaned_data