"""urls routing for fitnesspal."""

from django.urls import path
from . import views

app_name = 'fitnesspal'

urlpatterns = [
    path('', views.index, name='index'),
    path('calories/', views.calories, name='calories'),
    path('calories/search/', views.search_food, name='search_food'),
    path('calories/calculate/', views.calculate_calories, name='calculate_calories'),
    path('exercise/', views.exercise, name='exercise'),
    path('exercise/calculate/', views.exercise_calories_burn, name='calculate_exercise'),
    path('profile/', views.profile, name="profile"),
    path('profile/edit/', views.profile_edit, name="profile_edit"),
    path('calories/add/', views.add_food_calories, name="add_food"),
    path('exercise/add/', views.add_exercise, name="add_exercise"),
    path('profile/delete/food/', views.delete_food, name='delete_food'),
    path('profile/delete/exercise/', views.delete_exercise, name='delete_exercise')
]
