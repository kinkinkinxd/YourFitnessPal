"""Models class for database."""

from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """Class for profile models."""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    goal = models.IntegerField(default=0)
    age = models.IntegerField(default=0)
    gender = models.CharField(max_length=100, default='')
    weight = models.IntegerField(default=0)
    height = models.IntegerField(default=0)

    def __str__(self):
        """Return the user's first name."""
        return self.user.first_name


class Calories(models.Model):
    """Class for calories models."""

    food_name = models.CharField(max_length=100)
    unit = models.CharField(max_length=100, default='')
    calories = models.IntegerField(default=0)
    cholesterol = models.IntegerField(default=0)
    sodium = models.IntegerField(default=0)
    carbohydrates = models.IntegerField(default=0)
    diet_fiber = models.IntegerField(default=0)
    sugar = models.IntegerField(default=0)
    fats = models.IntegerField(default=0)
    sat_fats = models.IntegerField(default=0)
    tran_fats = models.IntegerField(default=0)
    vit_a = models.IntegerField(default=0)
    vit_c = models.IntegerField(default=0)
    calcium = models.IntegerField(default=0)
    iron = models.IntegerField(default=0)
    protein = models.IntegerField(default=0)
    weight = models.IntegerField(default=0)
    date = models.DateTimeField('date food added', null=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)

    def __str__(self):
        """Return the food name."""
        return self.food_name


class Exercise(models.Model):
    """Class for exercise models."""

    exercise_name = models.CharField(max_length=100)
    calories = models.IntegerField(default=0)
    duration = models.IntegerField(default=0)
    met = models.IntegerField(default=0)
    date = models.DateTimeField('date exercise add', null=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)

    def __str__(self):
        """Return the exercise name."""
        return self.exercise_name

