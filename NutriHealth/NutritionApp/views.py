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


def user_information(request, user_id):
    try:
        user_info = UserInformation.objects.get(author_id=user_id)
    except UserInformation.DoesNotExist:
        # Handle the case where the specified user ID does not exist
        return render(request, 'main/user-not-found.html')

    form = UserInformationForm()

    if request.method == 'POST':
        form = UserInformationForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.author_id = request.user.id  
            item.save()
            return redirect('main:index')  # Redirect to the index page after form submission

    return render(request, 'main/user-information.html', {"user_info": user_info, "form": form})