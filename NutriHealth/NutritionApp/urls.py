from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('about', views.about, name='about'),

    path('register', views.register, name='register'), # Register Page

    path('user-information/<int:user_id>/', views.user_information, name='user_information'),

    path('team', views.team, name='team'),

    path('contact-us', views.contact, name='contact_us'), # Contact Page

]