import os
import django
import pandas as pd

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "NutriHealth.settings")
django.setup()

# Now you can import your models
from NutritionApp.models import FoodItem

def populate_food_items_from_excel(file_path):
    # Read the Excel file into a DataFrame, skipping the first two rows
    df = pd.read_excel(file_path, header=None, skiprows=2)

    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        try:
            # Extract and validate data from the row
            code = row[0]
            name = row[1]
            serving_size = row[2]

            # Check if the necessary fields are not null
            if pd.notnull(row[4]) and pd.notnull(row[6]) and pd.notnull(row[8]):
                energy = float(row[4])
                protein = float(row[6])
                fat = float(row[7]) if not pd.isnull(row[7]) else 0  # Default to 0 if fat is missing
                carbohydrates = float(row[8])
            else:
                raise ValueError("Essential nutrient values are missing")

            # Create a FoodItem object and save it to the database
            food_item = FoodItem(
                code=code,
                name=name,
                serving_size=serving_size,
                energy=energy,
                protein=protein,
                fat=fat,
                carbohydrates=carbohydrates
            )
            food_item.save()
        except (ValueError, IndexError) as e:
            # Skip rows with invalid data or incomplete rows
            print(f"Skipping row {index + 2} due to invalid data or incomplete row: {e}")


# Example usage:
populate_food_items_from_excel(r'C:\Users\Caleb King\Desktop\Nutri\NutriHealth\NutriHealth\data-infromation\data.xlsx')
