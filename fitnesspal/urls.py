"""urls routing for fitnesspal."""

from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'fitnesspal'

urlpatterns = [
    path('', views.index, name='index'),
    path('calories/', views.calories, name='calories'),
    path('calories/calculate/', views.calculate_calories, name='calculate_calories'),
    path('exercise/', views.exercise, name='exercise'),
    path('exercise/calculate/', views.exercise_calories_burn, name='calculate_exercise')
    path('profile/', views.profile, name="profile"),
    path('calories/add/', views.add_food_calories, name="add_food"),
]

