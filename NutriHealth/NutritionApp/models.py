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