from django.contrib import admin
from .models import Contact
# Register your models here.


class ContactModel(admin.ModelAdmin):
    list_display = ['sno', 'name', 'phone', 'email', 'description', 'timestamp']


admin.site.register(Contact, ContactModel)
