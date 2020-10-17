from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse


from django.shortcuts import render


def index(request):
    return render(request, 'fitnesspal/index.html')
