# Import necessary modules
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "NutriHealth.settings")
django.setup()

# Import your Django models
from NutritionApp.models import RecomededIntake

# Function to generate sample data
def generate_sample_data():
    # Sample data for Dinner
    RecommendedIntake.objects.create(
        meal="Dinner",
        min_age=18,
        max_age=30,
        gender="Male",
        total_protein=28.0,  # in grams
        total_carbohydrates=65.0,  # in grams
        total_fat=20.0  # in grams
    )

    RecommendedIntake.objects.create(
        meal="Dinner",
        min_age=18,
        max_age=30,
        gender="Female",
        total_protein=25.0,  # in grams
        total_carbohydrates=60.0,  # in grams
        total_fat=18.0  # in grams
    )

    RecommendedIntake.objects.create(
        meal="Dinner",
        min_age=31,
        max_age=50,
        gender="Male",
        total_protein=30.0,  # in grams
        total_carbohydrates=70.0,  # in grams
        total_fat=23.0  # in grams
    )

    RecommendedIntake.objects.create(
        meal="Dinner",
        min_age=31,
        max_age=50,
        gender="Female",
        total_protein=28.0,  # in grams
        total_carbohydrates=65.0,  # in grams
        total_fat=20.0  # in grams
    )
