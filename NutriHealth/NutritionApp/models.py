from django.db import models

# Create your models here.
class UserInformation(models.Model):
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