"""urls routing for fitnesspal."""

from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'fitnesspal'

urlpatterns = [
    path('', views.index, name='index'),
    path('calories/', views.calories, name='calories'),
    path('calories/calculate/', views.calculate_calories, name='calculate_calories'),
    path('exercise/', views.ExerciseView.as_view(), name='exercise')
]

