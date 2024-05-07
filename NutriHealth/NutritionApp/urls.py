from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('register', views.register, name='register'), # Register Page

    path('user-information/<int:user_id>/', views.user_information, name='user_information'),


]