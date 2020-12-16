"""Admin class for this application admin."""
from django.contrib import admin

from .models import Calories, Exercise, Profile

admin.site.register(Calories)
admin.site.register(Exercise)
admin.site.register(Profile)
