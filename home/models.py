from django.db import models


# model for Contact

class Contact(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=13)
    email = models.EmailField(max_length=30)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)
