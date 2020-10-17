from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse


from django.shortcuts import render


def index(request):
    """Views for home page"""
    return render(request, 'fitnesspal/index.html')
