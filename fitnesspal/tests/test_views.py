"""Registration tests."""
from django.contrib.auth.models import User
from fitnesspal.models import Profile,Calories,Exercise
from django.test import TestCase
from django.shortcuts import reverse
from django.utils import timezone
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
        response = self.client.post(reverse('fitnesspal:calculate_exercise'), {'exercise-input': 'trampoline', 'weight': 60}, follow=True)  
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,'trampoline')
    
    def test_add_exercise(self):
        """Test if user can add an exercise and it will be added to the profile."""
        response = self.client.post(reverse('fitnesspal:calculate_exercise'), {'exercise-input': 'Trampoline', 'weight': 60}, follow=True)  
        response = self.client.post(reverse('fitnesspal:add_exercise'), {'add_exercise_button': 'Trampoline'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.profile.exercise_set.filter(exercise_name=self.exercise.exercise_name).exists())
    
class ProfileViewTest(TestCase):
    """Test for profile page."""

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
        self.exercise = Exercise.objects.create(exercise_name="Trampoline", calories = 52, user = self.profile, date=timezone.now())
        self.food = Calories.objects.create(food_name="chicken", unit = 1, calories = 187, user = self.profile, date=timezone.now())
        self.profile.goal = 2000

    def test_unauthenticated_cant_access(self):
        """Test that when unauthenticated user try to access profile page, it will redirect to login page."""
        response = self.client.get(reverse('logout'))
        response = self.client.post(reverse('fitnesspal:profile'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=%2Fprofile%2F')
    
    def test_added_exercise_is_shown(self):
        """Test that the added exercise will be shown on the profile page."""
        response = self.client.post(reverse('fitnesspal:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.profile.exercise_set.filter(exercise_name=self.exercise.exercise_name, user = self.profile).exists())

    def test_added_food_is_shown(self):
        """Test that the added food will be shown on the profile page."""
        response = self.client.post(reverse('fitnesspal:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.profile.calories_set.filter(food_name=self.food.food_name, user = self.profile).exists())

    def test_first_name_is_shown(self):
        """Test that the user's first name will be shown on the profile page."""
        response = self.client.post(reverse('fitnesspal:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,'tester')
    
    def test_calories_goal_is_shown(self):
        """Test that the user's calories goal will be shown on the profile page."""
        response = self.client.post(reverse('fitnesspal:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,'2000')
    
    def test_total_food_calories_is_shown(self):
        """Test that the user's total food calories will be shown on the profile page."""
        response = self.client.post(reverse('fitnesspal:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '187')

    def test_total_exercise_calories_is_shown(self):
        """Test that the user's total exercise calories will be shown on the profile page."""
        response = self.client.post(reverse('fitnesspal:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '52')

    def test_remaining_calories_is_shown(self):
        """Test that the user's remaining calories(goal - food - exercise) will be shown on the profile page."""
        response = self.client.post(reverse('fitnesspal:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '1865')