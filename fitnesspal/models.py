"""Models class for database."""
import datetime

from django.db import models
from django.utils import timezone

class Calories(models.Model):
    food_name = models.CharField(max_length=20)

    def __str__(self):
        return self.food_name

class Exercise(models.Model):
    exercise_name = models.CharField(max_length=20)

    def __str__(self):
        return self.exercise_name

class User(models.Model):
   user_name = models.CharField(max_length=40)
   password = models.CharField(max_length=20)
   food_eat = models.ManyToManyField(Calories)
   exercise = models.ManyToManyField(Exercise)

   def __str__(self):
        return self.user_name