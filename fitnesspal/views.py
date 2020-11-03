from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login
from django.views import generic

def index(request):
    return render(request, 'fitnesspal/index.html')


def calories(request):
    return render(request, 'fitnesspal/calories.html')


# def add_calories(request, calories_id):

