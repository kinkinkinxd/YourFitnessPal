"""Models tests."""
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from fitnesspal.models import Calories, Exercise, Profile


class CalorieModelTest(TestCase):
    """Class for calorie models."""

    def setUp(self):
        """Set up for calories models."""
        self.food = Calories.objects.create(food_name="chicken")
        self.food2 = Calories.objects.create(food_name="potato")

    def test_food_name(self):
        """Test str of food."""
        self.assertEqual(str(self.food), "chicken")
        self.assertEqual(str(self.food2), "potato")


class ExerciseModelTest(TestCase):
    """Class for exercise models."""

    def setUp(self):
        """Set up for exercise models."""
        self.exercise = Exercise.objects.create(exercise_name="soccer")
        self.exercise2 = Exercise.objects.create(exercise_name="yoga")

    def test_exercise_name(self):
        """Test str of exercise"""
        self.assertEqual(str(self.exercise), "soccer")
        self.assertEqual(str(self.exercise2), "yoga")


class ProfileModelTest(TestCase):
    """Class for profile models."""

    def setUp(self):
        """Set up for profile models."""
        self.user = {
            'username': 'tester',
            'first_name': 'tester',
            'email': 'test@gmail.com',
            'password': 'password',
        }
        self.username = User.objects.create_user(**self.user)
        self.profile = Profile.objects.create(user=self.username)

    def test_profile_name(self):
        """Test str of profile."""
        self.client.post(reverse('login'), self.user)
        self.assertEqual(str(self.profile), "tester")
