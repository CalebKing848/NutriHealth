import os
import django
import pandas as pd

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "NutriHealth.settings")
django.setup()

# Now you can import your models
from NutritionApp.models import FoodItem

def populate_food_items_from_excel(file_path):
    # Read the Excel file into a DataFrame, skipping the first three rows
    df = pd.read_excel(file_path, header=None, skiprows=4)

    # Check if there are at least four rows in the DataFrame
    if len(df) >= 5:
        # Extract the fourth row (index 3) from the DataFrame
        row = df.iloc[1]  # Fetching the next row after skipping 4 rows

        try:
            # Assuming the data in the row matches the fields in your FoodItem model
            code = row[0]
            name = row[1]
            serving_size = row[2]
            energy = float(row[3])
            protein = float(row[4])
            fat = float(row[5]) if not pd.isnull(row[5]) else 0  # Set default value to 0 if fat is not available
            carbohydrates = float(row[6])

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
        except (ValueError, IndexError):
            # Skip rows with invalid data or incomplete rows
            print(f"Skipping row 6 due to invalid data or incomplete row.")
    else:
        print("The Excel file does not contain enough rows.")

# Example usage:
populate_food_items_from_excel(r'\\19340372.hdrive.uict.nz\HDrive\19340372\Local\Desktop\Git v2\NutriHealth\NutriHealth\data-infromation\data.xlsx')


# def populate_food_items_from_excel(file_path, output_file):
#     # Read the Excel file into a DataFrame, skipping the first four rows
#     df = pd.read_excel(file_path, header=None, skiprows=4)

#     # Check if there are at least five rows in the DataFrame
#     if len(df) >= 5:
#         # Extract the sixth row (index 5) from the DataFrame
#         row = df.iloc[1]  # Fetching the next row after skipping 4 rows

#         try:
#             # Assuming the data in the row matches the fields in your FoodItem model
#             code = row[0]
#             name = row[1]
#             serving_size = row[2]
#             energy = float(row[3])
#             protein = float(row[4])
#             fat = float(row[5]) if not pd.isnull(row[5]) else 0  # Set default value to 0 if fat is not available
#             carbohydrates = float(row[6])

#             # Write the data to the output file
#             with open(output_file, 'w') as file:
#                 file.write(f"Code: {code}\n")
#                 file.write(f"Name: {name}\n")
#                 file.write(f"Serving Size: {serving_size}\n")
#                 file.write(f"Energy: {energy}\n")
#                 file.write(f"Protein: {protein}\n")
#                 file.write(f"Fat: {fat}\n")
#                 file.write(f"Carbohydrates: {carbohydrates}\n")
                
#             print("Data written to the output file successfully.")
#         except (ValueError, IndexError):
#             # Skip rows with invalid data or incomplete rows
#             print(f"Skipping row 6 due to invalid data or incomplete row.")
#     else:
#         print("The Excel file does not contain enough rows.")

# # Example usage:
# populate_food_items_from_excel(r'\\19340372.hdrive.uict.nz\HDrive\19340372\Local\Desktop\Git v2\NutriHealth\NutriHealth\data-infromation\data.xlsx', 'output.txt')