from django.contrib import admin

from .models import Calories, Exercise, User, Profile

admin.site.register(Calories)
admin.site.register(Exercise)
admin.site.register(Profile)
