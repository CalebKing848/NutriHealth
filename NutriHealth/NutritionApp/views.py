import datetime
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm, UserInformationForm, ContactInformationForm, FoodItemForm, DailyIntakeItemForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User  # Import the User model
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from .models import UserInformation, FoodItem, DailyIntakeItem, DailyIntake
from django.db.models import Sum, F
from matplotlib import pyplot as plt
from collections import defaultdict
import io
import base64


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



def generate_pie_chart(daily_intake_items):
    # Calculate total protein, carbohydrates, and fat
    total_protein = daily_intake_items.aggregate(
        total_protein=Sum(F('food_item__protein') * F('quantity'))
    )['total_protein'] or 0
    total_carbohydrates = daily_intake_items.aggregate(
        total_carbohydrates=Sum(F('food_item__carbohydrates') * F('quantity'))
    )['total_carbohydrates'] or 0
    total_fat = daily_intake_items.aggregate(
        total_fat=Sum(F('food_item__fat') * F('quantity'))
    )['total_fat'] or 0

    # Prepare data for pie chart
    labels = ['Total Protein', 'Total Carbohydrates', 'Total Fat']
    quantities = [total_protein, total_carbohydrates, total_fat]

    # Create pie chart
    plt.figure(figsize=(8, 8))
    plt.pie(quantities, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle

    # Save the pie chart to a BytesIO object
    image_stream = io.BytesIO()
    plt.savefig(image_stream, format='png')
    image_stream.seek(0)

    # Encode the image to base64 for embedding in HTML
    base64_image = base64.b64encode(image_stream.getvalue()).decode('utf-8')
    plt.close()

    return base64_image


def daily_intake(request, intake_id=None):
    user = request.user
    today = datetime.date.today()

    if intake_id:
        # If intake_id is provided, fetch the specific daily intake
        daily_intake = get_object_or_404(DailyIntake, pk=intake_id, user=user, date=today)
    else:
        # Ensure there is only one daily intake entry per user per day
        daily_intake, created = DailyIntake.objects.get_or_create(user=user, date=today)
        
        # Remove any extra entries if they exist
        extra_entries = DailyIntake.objects.filter(user=user, date=today).exclude(pk=daily_intake.pk)
        extra_entries.delete()

    if request.method == 'POST':
        form = DailyIntakeItemForm(request.POST)
        if form.is_valid():
            # Ensure the daily intake instance is saved before creating items
            if created:
                daily_intake.save()
            daily_intake_item = form.save(commit=False)
            daily_intake_item.daily_intake = daily_intake
            daily_intake_item.save()
            return redirect('daily_intake')
    else:
        form = DailyIntakeItemForm()

    daily_intake_items = daily_intake.items.all()

    # Perform aggregation for total protein, carbohydrates, and fat considering the quantity
    total_protein = daily_intake_items.aggregate(
        total_protein=Sum(F('food_item__protein') * F('quantity'))
    )['total_protein'] or 0
    total_carbohydrates = daily_intake_items.aggregate(
        total_carbohydrates=Sum(F('food_item__carbohydrates') * F('quantity'))
    )['total_carbohydrates'] or 0
    total_fat = daily_intake_items.aggregate(
        total_fat=Sum(F('food_item__fat') * F('quantity'))
    )['total_fat'] or 0

    # Generate pie chart
    pie_chart = generate_pie_chart(daily_intake_items)

    context = {
        'form': form,
        'daily_intake_items': daily_intake_items,
        'daily_intake': daily_intake,
        'total_protein': total_protein,
        'total_carbohydrates': total_carbohydrates,
        'total_fat': total_fat,
        'pie_chart': pie_chart,
    }
    return render(request, 'main/daily_intake.html', context)


@login_required
def save_daily_intake(request):
    user = request.user
    today = datetime.date.today()
    daily_intakes = DailyIntake.objects.filter(user=user, date=today)

    # Save the daily intake data here if needed

    return redirect('daily_intake')

@login_required
def delete_daily_intake_item(request, pk):
    daily_intake_item = get_object_or_404(DailyIntakeItem, pk=pk)
    daily_intake_item.delete()
    return redirect('daily_intake')


def saved_daily_intake(request):
    user = request.user
    saved_intakes = DailyIntake.objects.filter(user=user)
    context = {
        'saved_intakes': saved_intakes,
    }
    return render(request, 'main/saved_daily_intake.html', context)

