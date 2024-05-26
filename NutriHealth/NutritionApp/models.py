from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserInformation(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    age = models.IntegerField()  
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    weight = models.FloatField()
    height = models.FloatField() 
    energy_intake = models.IntegerField()
    existing_medical_conditions = models.TextField() 

class ContactInformation(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class FoodItem(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=200)
    serving_size = models.CharField(max_length=100)
    energy = models.FloatField()
    protein = models.FloatField()
    fat = models.FloatField()
    carbohydrates = models.FloatField()


class DailyIntake(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)

class DailyIntakeItem(models.Model):
    daily_intake = models.ForeignKey(DailyIntake, related_name='items', on_delete=models.CASCADE)
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    @property
    def total_calories(self):
        return self.food_item.calories * self.quantity

    @property
    def total_protein(self):
        return self.food_item.protein * self.quantity

    @property
    def total_carbohydrates(self):
        return self.food_item.carbohydrates * self.quantity

    @property
    def total_fat(self):
        return self.food_item.fat * self.quantity