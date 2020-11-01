from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import redirect, render


def signup(request):
    if request.method =='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('fitnesspal:index')
    else:
        form = UserCreationForm()
    return render(request, '../templates/registration/signup.html', {'form': form})
