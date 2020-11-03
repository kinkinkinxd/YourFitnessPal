"""Models class for database."""
import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Calories(models.Model):
    food_name = models.CharField(max_length=20)

    def __str__(self):
        return self.food_name


class Exercise(models.Model):
    exercise_name = models.CharField(max_length=20)

    def __str__(self):
        return self.exercise_name


class Profile(models.Model):
   user = models.OneToOneField(User, on_delete=models.CASCADE)
   food_eat = models.ManyToManyField(Calories)
   exercise = models.ManyToManyField(Exercise)

   def __str__(self):
        return self.user.get_full_name()