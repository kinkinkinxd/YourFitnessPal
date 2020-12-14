"""Registration tests."""
from django.contrib.auth.models import User
from fitnesspal.models import Profile,Calories,Exercise
from django.test import TestCase
from django.shortcuts import reverse
import unittest

class CaloriesViewTest(TestCase):
    """Test for calories page."""
    def setUp(self):
        self.user = {
            'username': 'tester',
            'first_name': 'tester',
            'email': 'test@gmail.com',
            'password': 'password'
        }
        self.username = User.objects.create_user(**self.user)
        self.profile = Profile.objects.filter(user=self.username).first()
        self.client.post(reverse('login'), self.user)
        self.food = Calories.objects.create(food_name="chicken")

    def test_searching_for_food(self):
        """Test if searching a food keyword in the input bar will give the list that contain the food."""
        response = self.client.post(reverse('fitnesspal:search_food'), {'food-input': 'chicken'}, follow=True)  
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "chicken")

class ExerciseViewTest(TestCase):
    """Test for calories page."""

    def setUp(self):
        self.user = {
            'username': 'tester',
            'first_name': 'tester',
            'email': 'test@gmail.com',
            'password': 'password'
        }
        self.username = User.objects.create_user(**self.user)
        self.profile = Profile.objects.filter(user=self.username).first()
        self.client.post(reverse('login'), self.user)
        self.exercise = Exercise.objects.create(exercise_name="Trampoline")

    def test_searching_for_exercise(self):
        """Test if searching an exercise keyword in the input bar will give the data of that exercise."""
        response = self.client.post(reverse('fitnesspal:calculate_exercise'), {'exercise-input': 'Trampoline', 'weight': 60}, follow=True)  
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Trampoline")
    
    def test_add_exercise(self):
        response = self.client.post(reverse('fitnesspal:calculate_exercise'), {'exercise-input': 'Trampoline', 'weight': 60}, follow=True)  
        response = self.client.post(reverse('fitnesspal:add_exercise'), {'add_exercise_button': 'Trampoline'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.profile.exercise_set.filter(exercise_name=self.exercise.exercise_name).exists())