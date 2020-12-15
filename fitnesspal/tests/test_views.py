import unittest

from django.test import TestCase
from django.urls import reverse
from fitnesspal.models import Profile, Calories
from django.contrib.auth.models import User
from fitnesspal.views import search_nutrients_from_nl_query


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

    def test_authenticated_adding_food(self):
        response = self.client.post(reverse('fitnesspal:add_food'), {'add_button': 'chicken'}, follow=True)
        self.assertIs(response.context['user'].is_authenticated, True)
        self.assertIs(self.profile.calories_set.filter(food_name=self.food.food_name).exists(), True)

    def test_not_authenticated_adding_food(self):
        self.client.post(reverse('logout'))
        response = self.client.post(reverse('fitnesspal:add_food'), {'add_button': 'chicken'}, follow=True)
        self.assertIs(response.context['user'].is_authenticated, False)
        self.assertEquals(response.status_code, self.client.get(reverse('login')).status_code)

    def test_search_nutrients(self):
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

    # def test_get_nutrient(self):


if __name__ == '__main__':
    unittest.main()
