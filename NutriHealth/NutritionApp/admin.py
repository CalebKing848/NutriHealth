from django.contrib import admin

from .models import UserInformation
from .models import ContactInformation


# Register your models here.
admin.site.register(UserInformation)
admin.site.register(ContactInformation)
