"""urls routing for fitnesspal."""
from django.contrib import admin
from django.urls import path, include

from . import views


app_name = 'fitnesspal'
urlpatterns = [path('admin/', admin.site.urls),
    path('signup/', views.signup_view, name='signup'),
]