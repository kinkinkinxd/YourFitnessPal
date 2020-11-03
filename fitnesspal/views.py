from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login

def index(request):
    return render(request, 'fitnesspal/index.html')
