from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm, UserInformationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User  # Import the User model
from .forms import UserInformationForm, ContactInformationForm, FoodItemForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
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
    query = request.GET.get('q')
    if query:
        foods_list = FoodItem.objects.filter(name__icontains=query)
    else:
        foods_list = FoodItem.objects.all()

    paginator = Paginator(foods_list, 10)  # Show 10 food items per page
    page_number = request.GET.get('page')

    try:
        foods = paginator.page(page_number)
    except PageNotAnInteger:
        foods = paginator.page(1)
    except EmptyPage:
        foods = paginator.page(paginator.num_pages)

    if request.method == 'POST':
        form = FoodItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('nutrition_database')
    else:
        form = FoodItemForm()

    return render(request, 'main/nutrition_database.html', {"foods": foods, "query": query, "form": form})

def update_food_item(request, pk):
    food_item = get_object_or_404(FoodItem, pk=pk)
    if request.method == 'POST':
        form = FoodItemForm(request.POST, instance=food_item)
        if form.is_valid():
            form.save()
            return redirect('nutrition_database')
    else:
        form = FoodItemForm(instance=food_item)
    return render(request, 'main/nutrition_database.html', {"form": form})

def delete_food_item(request, pk):
    food_item = get_object_or_404(FoodItem, pk=pk)
    if request.method == 'POST':
        food_item.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})




def daily_intake(request):
    return render(request, 'main/daily_intake.html')

def saved_daily_intake(request):
    return render(request, 'main/saved_daily_intake.html')

