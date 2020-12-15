from time import timezone

from django.shortcuts import render
from django.contrib import messages
from datetime import date
from .models import Calories, Exercise, Profile
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


def daily_value(quantity, rec_quantity, ):
    """Calculate % daily value for the nutrition.
    Args:
        quantity: quantity of value
        rec_quantity: recommend quantity of value

    Returns:
        % daily value for the nutrition
    """
    return (quantity / rec_quantity) * 100


def exercise(request):
    """Exercise views."""
    return render(request, 'fitnesspal/exercise.html')


def index(request):
    """Index views."""
    return render(request, 'fitnesspal/index.html')


def calories(request):
    """Calories views."""
    return render(request, 'fitnesspal/calories.html')


def search_nutrients_from_nl_query(
        query: str,
        num_servings: float = None,
        aggregate: bool = None,
        line_delimited: bool = None) -> requests.Response:
    """Returns the nutrients for all foods in the posted query.

    Get detailed nutrient breakdown of any natural language text.

    Args:
        query: the query string. Required.
        num_servings: the number of servings this dish yields. The nutrients when this food is logged will be divided by this number.
        aggregate: if present, it combines all the foods into one food object with the food_name equal to the value of this field
        line_delimited: if present, it expects only 1 food per line and will return an array of rules broken if there are any. i.e. 2+ foods on a line, no foods detected on this line, etc

    Returns:
        Response
    """
    endpoint = '/v2/search/instant?query=$' + query
    # Set the headers
    headers = HEADER
    # Normally I would just use **kwargs to hold the values, but making it verbose is easier for users
    body = {
        "query": query,
        "num_servings": num_servings,
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


def get_nutrients_from_nl_query(
        query: str,
        num_servings: float = None,
        aggregate: bool = None,
        line_delimited: bool = None) -> requests.Response:
    """Returns the nutrients for all foods in the posted query.
    Get detailed nutrient breakdown of any natural language text.

    Args:
        query: the query string. Required.
        num_servings: the number of servings this dish yields. The nutrients when this food is logged will be divided by this number.
        aggregate: if present, it combines all the foods into one food object with the food_name equal to the value of this field
        line_delimited: if present, it expects only 1 food per line and will return an array of rules broken if there are any. i.e. 2+ foods on a line, no foods detected on this line, etc
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


def search_food(request):
    food_list = []
    try:
        res = search_nutrients_from_nl_query(query=request.POST["food-input"])
    except AssertionError:
        messages.warning(request, "Result not found")
        return render(request, 'fitnesspal/calories.html')
    else:
        for i in range(30):
            try:
                res.json()["common"][i]["food_name"]
            except IndexError:
                if i == 0:
                    messages.warning(request, "Result not found")
                break
            else:
                food_list.append(res.json()["common"][i]["food_name"])
    return render(request, 'fitnesspal/calories.html', {'food_list': food_list})


def calculate_calories(request):
    food_size = 1
    food_name = request.GET["parameter"]
    if request.POST.get('food_size') is not None:
        food_size = request.POST.get('food_size')
    query = f"{food_size} {food_name}"
    try:
        res = get_nutrients_from_nl_query(query=query)
    except AssertionError:
        messages.warning(request, "Result not found")
        print(1)
        return render(request, 'fitnesspal/calories.html')
    else:
        try:
            food_dict = res.json()["foods"][0]["full_nutrients"]
            nutrients = {'protein': 203, 'tol_fats': 204, 'carb': 208, 'cal': 208, 'sugar': 269, 'diet_fiber': 291,
                         'calcium': 301, 'iron': 303, 'sodium': 307, 'vit_a': 320, 'vit_c': 401, 'cholesterol': 601,
                         'tran_fats': 605, 'sat_fats': 606}
            result_dict = {}
            for num in range(len(food_dict)):
                for key, value in nutrients.items():
                    if food_dict[num]['attr_id'] == value:
                        result_dict[key] = food_dict[num]['value']
            for key in nutrients.keys():
                if key not in result_dict.keys():
                    result_dict[key] = 0
            name = res.json()["foods"][0]["food_name"]
            weight = res.json()["foods"][0]['serving_weight_grams']
            unit = res.json()["foods"][0]['serving_unit']
            pic = res.json()["foods"][0]["photo"]["thumb"]
            dv_fat = daily_value(result_dict['tol_fats'], 78)
            dv_sat = daily_value(result_dict['sat_fats'], 20)
            dv_cholesterol = daily_value(result_dict['cholesterol'], 300)
            dv_sodium = daily_value(result_dict['sodium'], 2300)
            dv_carb = daily_value(result_dict['carb'], 275)
            dv_fiber = daily_value(result_dict['diet_fiber'], 28)
            iron = daily_value(result_dict['iron'], 18)
            vit_a = daily_value(result_dict['vit_a'], 900)
            vit_c = daily_value(result_dict['vit_c'], 500)
            calcium = daily_value(result_dict['calcium'], 1300)
            cal_from_fat = result_dict['tol_fats'] * 9
            new_food = Calories.objects.create(food_name=name, calories=result_dict['cal'],
                                               carbohydrates=result_dict['carb'], fats=result_dict['tol_fats'],
                                               unit=unit, sat_fats=result_dict['sat_fats'],
                                               tran_fats=result_dict['tran_fats'], sugar=result_dict['sugar'],
                                               diet_fiber=result_dict['diet_fiber'], iron=iron,
                                               sodium=result_dict['sodium'], vit_a=vit_a,
                                               vit_c=vit_c, cholesterol=result_dict['cholesterol'],
                                               protein=result_dict['protein'], calcium=calcium,
                                               weight=weight, date=timezone.now())
            context = {'new_food': new_food, 'pic': pic, 'cal_from_fat': cal_from_fat, 'dv_fat': dv_fat,
                       'dv_sat': dv_sat, 'dv_cholesterol': dv_cholesterol, 'dv_sodium': dv_sodium, 'dv_carb': dv_carb,
                       'dv_fiber': dv_fiber, 'food_name': food_name, 'food_size': food_size}
        except KeyError:
            messages.warning(request, "Result not found")
            return render(request, 'fitnesspal/calories.html')
        else:
            return render(request, 'fitnesspal/calories_result.html', context=context)


def exercise_calories_burn(request):
    try:
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
    context = {'total_food': total_food, 'total_cal': total_cal, 'total_exercise': total_exercise, 'food_cal': food_cal,
               'exercise_cal': exercise_cal}
    return render(request, 'fitnesspal/profile.html', context=context)


@login_required
def profile_edit(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return render(request, 'fitnesspal/profile_edit.html', {'u_form': u_form, 'p_form': p_form})
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'fitnesspal/profile_edit.html', context=context)
