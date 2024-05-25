from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('about', views.about, name='about'),

    path('register', views.register, name='register'), # Register Page

    path('user-information/<int:user_id>/', views.user_information, name='user_information'),

    path('team', views.team, name='team'),

    path('contact-us', views.contact, name='contact_us'), # Contact Page

    path('dashboard', views.dashboard, name='dashboard'), # Dashbaord Page

    path('nutrition_database', views.nutrition_database, name='nutrition_database'), # Dashbaord Page

    path('daily_intake', views.daily_intake, name='daily_intake'), # Daily Intake Page

    path('saved_daily_intake', views.saved_daily_intake, name='saved_daily_intake'), # Saved Daily Intake Page

    path('update_food_item/<int:pk>/', views.update_food_item, name='update_food_item'),
    path('delete_food_item/<int:pk>/', views.delete_food_item, name='delete_food_item')

]