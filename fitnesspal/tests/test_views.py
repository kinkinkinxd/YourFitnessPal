"""Registration tests."""
from django.contrib.auth.models import User
from fitnesspal.models import Profile, Calories, Exercise
from django.test import TestCase
from django.shortcuts import reverse
from django.utils import timezone
from fitnesspal.views import search_nutrients_from_nl_query, get_nutrients_from_nl_query


class CaloriesViewTest(TestCase):
    """Test for calories page."""

    def setUp(self):
        """Set up for tests."""
        self.user = {
            'username': 'tester',
            'first_name': 'tester',
            'email': 'test@gmail.com',
            'password': 'password'
        }
        self.username = User.objects.create_user(**self.user)
        self.profile = Profile.objects.create(user=self.username)
        self.client.post(reverse('login'), self.user)
        self.food = Calories.objects.create(food_name="chicken")

    def test_searching_for_food(self):
        """Test if searching a food keyword in the input bar will give the list that contain the food."""
        response = self.client.post(reverse('fitnesspal:search_food'), {'food-input': 'chicken'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "chicken")

    def test_search_nutrients(self):
        """Test search food in database api."""
        food_list = []
        check_list = ['chicken', 'chicken thigh', 'chicken wings', 'chicken broth', 'chicken salad', 'baked chicken',
                      'fried chicken', 'whole chicken', 'chicken curry', 'ground chicken', 'chicken cutlet',
                      'grilled chicken', 'chicken breasts', 'chicken sandwich', 'rotisserie chicken',
                      'baked chicken breast', 'grilled chicken breast', 'breaded chicken breast',
                      'baked breaded chicken breast', 'coconut breaded chicken breast']
        res = search_nutrients_from_nl_query('chicken')
        for i in range(30):
            try:
                res.json()["common"][i]["food_name"]
            except IndexError:
                if i == 0:
                    break
            else:
                food_list.append(res.json()["common"][i]["food_name"])
        self.assertEquals(food_list, check_list)

    def test_food_nutrition(self):
        """Test nutrition in api"""
        res = get_nutrients_from_nl_query("chicken")
        self.assertEqual(res.json()["foods"][0]["food_name"], 'chicken')
        self.assertEqual(res.json()["foods"][0]["nf_calories"], 187)

    def test_authenticated_adding_food(self):
        """Test adding food when authenticated."""
        response = self.client.post(reverse('fitnesspal:add_food'), {'add_button': 'chicken'}, follow=True)
        self.assertIs(response.context['user'].is_authenticated, True)
        self.assertIs(self.profile.calories_set.filter(food_name=self.food.food_name).exists(), True)


class ExerciseViewTest(TestCase):
    """Test for calories page."""

    def setUp(self):
        """Set up for tests."""
        self.user = {
            'username': 'tester',
            'first_name': 'tester',
            'email': 'test@gmail.com',
            'password': 'password'
        }
        self.username = User.objects.create_user(**self.user)
        self.profile = Profile.objects.create(user=self.username)
        self.client.post(reverse('login'), self.user)
        self.exercise = Exercise.objects.create(exercise_name="Trampoline")

    def test_searching_for_exercise(self):
        """Test if searching an exercise keyword in the input bar will give the data of that exercise."""
        response = self.client.post(reverse('fitnesspal:calculate_exercise'),
                                    {'exercise-input': 'trampoline', 'weight': 60}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'trampoline')

    def test_add_exercise(self):
        """Test if user can add an exercise and it will be added to the profile."""
        response = self.client.post(reverse('fitnesspal:calculate_exercise'),
                                    {'exercise-input': 'Trampoline', 'weight': 60}, follow=True)
        response = self.client.post(reverse('fitnesspal:add_exercise'), {'add_exercise_button': 'Trampoline'},
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.profile.exercise_set.filter(exercise_name=self.exercise.exercise_name).exists())


class ProfileViewTest(TestCase):
    """Test for profile page."""

    def setUp(self):
        """Set up for tests."""
        self.user = {
            'username': 'tester',
            'first_name': 'tester',
            'email': 'test@gmail.com',
            'password': 'password'
        }
        self.username = User.objects.create_user(**self.user)
        self.profile = Profile.objects.create(user=self.username, goal = 2000)
        self.client.post(reverse('login'), self.user)
        self.exercise = Exercise.objects.create(exercise_name="Trampoline", calories=52, user=self.profile,
                                                date=timezone.now())
        self.food = Calories.objects.create(food_name="chicken", unit=1, calories=187, user=self.profile,
                                            date=timezone.now())


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
        self.assertTrue(
            self.profile.exercise_set.filter(exercise_name=self.exercise.exercise_name, user=self.profile).exists())

    def test_added_food_is_shown(self):
        """Test that the added food will be shown on the profile page."""
        response = self.client.post(reverse('fitnesspal:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.profile.calories_set.filter(food_name=self.food.food_name, user=self.profile).exists())

    def test_first_name_is_shown(self):
        """Test that the user's first name will be shown on the profile page."""
        response = self.client.post(reverse('fitnesspal:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'tester')

    def test_calories_goal_is_shown(self):
        """Test that the user's calories goal will be shown on the profile page."""
        response = self.client.post(reverse('fitnesspal:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '2000')

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


class ProfileEditViewTest(TestCase):
    """Test for profile edit test"""

    def setUp(self):
        """Set up for tests."""
        self.user = {
            'username': 'tester',
            'first_name': 'tester',
            'email': 'test@gmail.com',
            'password': 'password'
        }
        self.username = User.objects.create_user(**self.user)
        self.profile = Profile.objects.create(user=self.username)
        self.client.post(reverse('login'), self.user)
        self.exercise = Exercise.objects.create(exercise_name="Trampoline", calories=52, user=self.profile,
                                                date=timezone.now())
        self.food = Calories.objects.create(food_name="chicken", unit=1, calories=187, user=self.profile,
                                            date=timezone.now())
        self.profile.weight = 70
        self.profile.height = 180

    def test_check_bmi(self):
        """Test calculate BMI in profile edit."""
        self.assertEqual(round(self.profile.weight/(self.profile.height/100)**2, 2), 21.6)

    def test_unauthenticated_access(self):
        """Test if unauthenticated user acess to edit profile page,It will redirect to login page."""
        self.client.post(reverse('logout'))
        response = self.client.get(reverse('fitnesspal:profile_edit'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/accounts/login/?next=/profile/edit/")
        self.assertRedirects(response, '/accounts/login/?next=%2Fprofile%2Fedit%2F')
