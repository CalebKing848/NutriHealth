from django.shortcuts import render, redirect
from .forms import RegisterForm, UserInformationForm
from django.contrib.auth import login, logout, authenticate

from .models import UserInformation

def home(request):
    return render(request, 'main/index.html')

# View for sign up page
def register(request): 
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/login')
        else:
            return render(request, 'registration/register.html', {"form": form}) # Returns the register page and the reigster Form
    form = RegisterForm() # Loads the Register Form
    return render(request, 'registration/register.html', {"form": form}) # Returns the register page and the reigster Form


def user_infromation(request):
    user_info = UserInformation.objects.all()
    form = UserInformationForm(request.POST)
    if form.is_valid():
        item = form.save(commit=False)
        item.save()
        return render(request, 'main/index.html', {"form": form})
    return render(request, 'main/user-infromation.html', {"UserInformation": user_info, "form": form})