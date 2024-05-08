from django.shortcuts import render, redirect
from .forms import RegisterForm, UserInformationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User  # Import the User model
from .models import UserInformation
from .forms import UserInformationForm


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

@login_required(login_url="/login")
def user_information(request, user_id):
   
    if request.user.id == user_id:

        user_info = UserInformation.objects.get(author_id=user_id)

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
        return render(request, 'main/user-information.html', {"user_info": user_info, "form": form})
    else:
        return render(request, 'registration/register.html')
    

def contact(request):
    return render(request, 'main/contact.html')