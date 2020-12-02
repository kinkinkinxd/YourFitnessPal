from time import timezone

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login
from django.views import generic
from django.contrib import messages
from django.utils import timezone
from datetime import date
from .models import Calories,Exercise,Profile
from .forms import UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required

import requests
from django.utils import timezone

BASE_URL = 'https://trackapi.nutritionix.com'

HEADER = {
    'Content-Type': 'application/json',  # Set the type of the body sent
    'x-app-id': "73ada124",  # Your Nutritionix Applicatoin ID
    'x-app-key': "679449fb041e2ca7f0fdfc02dc121d9a",  # Your Nutritionix Application Key
    'x-remote-user-id': '0'  # USe 0 for development according to the docs
}


def exercise(request):
    return render(request, 'fitnesspal/exercise.html')


def index(request):
    return render(request, 'fitnesspal/index.html')


def calories(request):
    return render(request, 'fitnesspal/calories.html')


# def profile_edit(request):
#     return render(request, 'fitnesspal/profile_edit.html')


def is_valid_locale(locale: str) -> bool:
    return locale in ['en_US', 'en_GB', 'de_DE', 'fr_FR', 'es_ES']


def get_nutrients_from_nl_query(
        query: str,
        num_servings: float = None,
        aggregate: bool = None,
        line_delimited: bool = None,
        use_raw_foods: bool = None,
        include_subrecipe: bool = None,
        timezone: str = None,
        consumed_at: str = None,
        lat: float = None,
        lng: float = None,
        meal_type: int = None,
        use_branded_foods: bool = None,
        locale: str = None) -> requests.Response:
    """Returns the nutrients for all foods in the posted query.

    Get detailed nutrient breakdown of any natural language text.

    Args:
        query: the query string. Required.
        num_servings: the number of servings this dish yields. The nutrients when this food is logged will be divided by this number.
        aggregate: if present, it combines all the foods into one food object with the food_name equal to the value of this field
        line_delimited: if present, it expects only 1 food per line and will return an array of rules broken if there are any. i.e. 2+ foods on a line, no foods detected on this line, etc
        use_raw_foods: Allows parsing of uncooked variants.
        include_subrecipe: if present, will return recipe composition of the requested food (if exists)
        timezone: timezone in which to parse relative time queries like “yesterday I ate x”
        consumed_at: ISO 8601 compliant date format. Will overwrite any interpreted time contexts.
        lat: latitude
        lng: longitude
        meal_type: meal type
        use_branded_foods: toggle interpretation of branded foods
        locale: locale value for natural food search. Supported values en_US, en_GB, de_DE, fr_FR, es_ES.

    Returns:
        Response
    """
    endpoint = '/v2/natural/nutrients'
    # Set the headers
    headers = HEADER
    # Normally I would just use **kwargs to hold the values, but making it verbose is easier for users
    body = {
        "query": query,
        "num_servings": num_servings,
        "aggregate": aggregate,
        "line_delimited": line_delimited,
        "use_raw_foods": use_raw_foods,
        "include_subrecipe": include_subrecipe,
        "timezone": timezone,
        "consumed_at": consumed_at,
        "lat": lat,
        "lng": lng,
        "meal_type": meal_type,
        "use_branded_foods": use_branded_foods,
        "locale": locale,
    }
    # remove values that aren't set
    for k in [k for k, v in body.items() if v is None]:
        body.pop(k)
    # send a POST request with specified headers and body to API end point
    response = requests.post(url=BASE_URL + endpoint, json=body, headers=headers)
    if response.status_code == 200:
        # Operation successful
        return response
    if response.status_code == 400:
        # Validation error
        return response
    if response.status_code == 500:
        # Base error
        return response
    raise AssertionError('Undocumented response status code')


def get_exercise_from_nl_query(
        query: str,
        gender: str = None,
        weight_kg: float = None,
        height_cm: float = None,
        age: int = None,
        aggregate: bool = None,
        line_delimited: bool = None) -> requests.Response:
    """Returns the exercise in the posted query.

        Get detailed nutrient breakdown of any natural language text.

        Args:
            query: the query string. Required.
            gender: the gender of the user
            weight_kg: the weight of the user
            height_cm:the height of the user
            age: the age of the user
            aggregate: if present, it combines all the exercise into one exercise object with the exercise_name equal to the value of this field
            line_delimited: if present, it expects only 1 exercise per line and will return an array of rules broken if there are any. i.e. 2+ exercise on a line, no exercise detected on this line, etc

        Returns:
            Response
        """

    endpoint = '/v2/natural/exercise'
    # Set the headers
    headers = HEADER
    # Normally I would just use **kwargs to hold the values, but making it verbose is easier for users
    body = {
        "query": query,
        "gender": gender,
        "weight_kg": weight_kg,
        "height_cm": height_cm,
        "age": age,
        "aggregate": aggregate,
        "line_delimited": line_delimited,
    }
    # remove values that aren't set
    for k in [k for k, v in body.items() if v is None]:
        body.pop(k)
    # send a POST request with specified headers and body to API end point
    response = requests.post(url=BASE_URL + endpoint, json=body, headers=headers)
    if response.status_code == 200:
        # Operation successful
        return response
    if response.status_code == 400:
        # Validation error
        return response
    if response.status_code == 500:
        # Base error
        return response
    raise AssertionError('Undocumented response status code')


def calculate_calories(request):
    try:
        res = get_nutrients_from_nl_query(query=request.POST["food-input"])
    except AssertionError:
        messages.warning(request, "Result not found")
        return render(request, 'fitnesspal/calories.html')
    else:
        try :
            cal = res.json()["foods"][0]["nf_calories"]
            name = res.json()["foods"][0]["food_name"]
            carb = res.json()["foods"][0]["nf_total_carbohydrate"]
            fats = res.json()["foods"][0]["nf_total_fat"]
            protein = res.json()["foods"][0]["nf_protein"]
            weight = res.json()["foods"][0]['serving_weight_grams']
            pic = res.json()["foods"][0]["photo"]["thumb"]
            new_food = Calories.objects.create(food_name = name, calories = cal, carbohydrates = carb,  fats = fats, protein = protein, weight = weight, date = timezone.now())
        except KeyError:
            messages.warning(request, "Result not found")
            return render(request, 'fitnesspal/calories.html')
        else:
            return render(request, 'fitnesspal/calories.html', {'new_food' : new_food, 'pic': pic})


def exercise_calories_burn(request):
    try:
        if request.POST["weight"] == '':
            # res = get_exercise_from_nl_query(query=request.POST["exercise-input"])
            messages.warning(request, "Please input weight")
            return render(request, 'fitnesspal/exercise.html')

        else:
            res = get_exercise_from_nl_query(query=request.POST["exercise-input"]
                                             , weight_kg=request.POST["weight"])
    except AssertionError:
        messages.warning(request, "Result not found")
        return render(request, 'fitnesspal/exercise.html')
    else:
        try:
            cal = res.json()["exercises"][0]["nf_calories"]
            name = res.json()["exercises"][0]["name"]
            duration = res.json()["exercises"][0]["duration_min"]
            met = res.json()["exercises"][0]["met"]
            new_exercise = Exercise.objects.create(exercise_name=name, calories=cal,
                                                   duration=duration, met=met, date=timezone.now())
        except IndexError:
            messages.warning(request, "Result not found")
            return render(request, 'fitnesspal/exercise.html')
        except KeyError:
            messages.warning(request, "Result not found")
            return render(request, 'fitnesspal/exercise.html')
        else:
            return render(request, 'fitnesspal/exercise.html',
                          {'new_exercise': new_exercise})

@login_required
def add_food_calories(request):
    food = Calories.objects.filter(food_name=request.POST['add_button']).last()
    profile = Profile.objects.filter(user=request.user).first()
    profile.calories_set.add(food)
    messages.success(request, f'This food has been added to your account!')
    return render(request, 'fitnesspal/calories.html')

@login_required
def add_exercise(request):
    exercise = Exercise.objects.filter(exercise_name=request.POST['add_exercise_button']).last()
    profile = Profile.objects.filter(user=request.user).first()
    profile.exercise_set.add(exercise)
    messages.success(request, f'This exercise has been added to your account!')
    return render(request, 'fitnesspal/exercise.html')

@login_required
def profile(request):
    profile = Profile.objects.filter(user=request.user).first()
    today = date.today()
    total_food = Calories.objects.filter(user=profile, date__year=today.year, date__month=today.month,
                                         date__day=today.day).all()
    total_exercise = Exercise.objects.filter(user=profile, date__year=today.year, date__month=today.month,
                                             date__day=today.day).all()
    total_cal = request.user.profile.goal
    exercise_cal = 0
    food_cal = 0
    for food in total_food:
        food_cal += food.calories
    for exercises in total_exercise:
        exercise_cal += exercises.calories
    total_cal = total_cal - food_cal + exercise_cal
    return render(request, 'fitnesspal/profile.html', {'total_food': total_food, 'total_cal': total_cal,
                                                       'total_exercise': total_exercise, 'food_cal': food_cal,
                                                       'exercise_cal': exercise_cal})

@login_required 
def profile_edit(request):

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return render(request, 'fitnesspal/profile_edit.html', {'u_form': u_form,'p_form': p_form})
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'fitnesspal/profile_edit.html', context)
