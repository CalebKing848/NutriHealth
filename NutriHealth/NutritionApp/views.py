from django.shortcuts import render, redirect
from .forms import RegisterForm, UserInformationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User  # Import the User model
from .forms import UserInformationForm, ContactInformationForm

from .models import UserInformation

from .models import FoodItem


def home(request):
    return render(request, 'main/home.html')

def about(request):
    return render(request, 'main/about.html')


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

@login_required(login_url="/login")
def user_information(request, user_id):
    # Check if the logged-in user matches the requested user_id
    if request.user.id == user_id:
        try:
            # Attempt to get the UserInformation object
            user_info = UserInformation.objects.get(author_id=user_id)
        except UserInformation.DoesNotExist:
            # Handle the case where UserInformation does not exist
            user_info = None
        
        if request.method == 'POST':
            if user_info:
                form = UserInformationForm(request.POST, instance=user_info)
            else:
                form = UserInformationForm(request.POST)   
            if form.is_valid():
                item = form.save(commit=False)
                item.author_id = request.user.id
                item.save()
                return redirect('/') 
        else:  
            if user_info:
                form = UserInformationForm(instance=user_info)
            else:
                form = UserInformationForm()
        return render(request, 'user-info/user-information.html', {"user_info": user_info, "form": form})
    else:
        return render(request, 'user-info/user-denied.html')
    

def team(request):
    return render(request, 'main/team.html')

    

def contact(request):

    if request.method == 'POST':
        form = ContactInformationForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.save()
            return redirect('/') 
    else:
        form = ContactInformationForm()
    return render(request, 'user-contact/contact.html', {"form": form})

def dashboard(request):
    return render(request, 'main/dashboard.html')
    
def nutrition_database(request):
    foods = FoodItem.objects.all()
    return render(request, 'main/nutrition_database.html', {"foods": foods})


def daily_intake(request):
    return render(request, 'main/daily_intake.html')

def saved_daily_intake(request):
    return render(request, 'main/saved_daily_intake.html')

