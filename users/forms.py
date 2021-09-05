from django import forms
from .models import user
from phonenumber_field.modelfields import PhoneNumberField
#from django.contrib.auth.models import User
#from django.contrib.auth.forms import UserCreationForm

"""
class UserRegisterForm(UserCreationForm):
	email = forms.EmailField()

	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']
"""

class UserRegisterForm(forms.ModelForm):
	nohp = PhoneNumberField()
	password = forms.CharField(widget=forms.PasswordInput())
	confirm_password = forms.CharField(widget=forms.PasswordInput())
	class Meta:
		model = user
		fields = ['name','email','nohp','password','confirm_password']
	def clean(self):
		cleaned_data = super(UserRegisterForm, self).clean()
		password = cleaned_data.get("password")
		confirm_password = cleaned_data.get("confirm_password")

		if password != confirm_password:
			self.add_error('confirm_password', "Password does not match")

		return cleaned_data
	
	def clean_email(self):
		cleaned_data = super(UserRegisterForm, self).clean()
		email = cleaned_data.get('email')
		try:
			match = user.objects.get(email = email)
			self.add_error('email', "This email address is already in use")
		except:
			return email