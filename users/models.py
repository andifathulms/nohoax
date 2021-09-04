from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class user(models.Model):
	id = models.BigAutoField(primary_key=True)
	name = models.CharField(max_length=50)
	email = models.EmailField()
	nohp = PhoneNumberField()
	password = models.CharField(max_length=50)
	dateJoin = models.DateTimeField(auto_now_add=True)
	lastLogin = models.DateTimeField(auto_now_add=True)