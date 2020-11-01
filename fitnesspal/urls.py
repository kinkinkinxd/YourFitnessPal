"""urls routing for fitnesspal."""
from django.urls import path
from . import views

app_name = 'fitnesspal'
urlpatterns = [
    path('', views.index, name='index'),
    path('calories/', views.calories, name="calories"),
]
