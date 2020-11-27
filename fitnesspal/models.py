"""Models class for database."""
import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(default=0)
    gender = models.CharField(max_length=100, default='')
    weight = models.IntegerField(default=0)
    height = models.IntegerField(default=0)

    def __str__(self):
        return self.user


class Calories(models.Model):
    food_name = models.CharField(max_length=20)
    calories = models.IntegerField(default=0)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.food_name


class Exercise(models.Model):
    exercise_name = models.CharField(max_length=20)
    calories = models.IntegerField(default=0)
    duration = models.IntegerField(default=0)
    met = models.IntegerField(default=0)
    date = models.DateTimeField('date exercise add', null=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.exercise_name
