import pandas as pd
from your_app.models import FoodItem

def populate_food_items_from_excel(file_path):
    # Read the Excel file into a DataFrame
    df = pd.read_excel(file_path, header=None)  # Assuming there's no header in the Excel file

    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        # Assuming the data in each row matches the fields in your FoodItem model
        code = row[0]
        name = row[1]
        serving_size = row[2]
        energy = row[3]
        protein = row[4]
        fat = row[5]
        carbohydrates = row[6]

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

# Example usage:
populate_food_items_from_excel("\\19340372.hdrive.uict.nz\HDrive\19340372\Local\Desktop\Git v2\NutriHealth\NutriHealth\food_data\food.xlsx")