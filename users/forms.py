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
			self.add_error('email', "Email ini telah digunakan")
		except:
			return email

	def clean_nohp(self):
		cleaned_data = super(UserRegisterForm, self).clean()
		nohp = cleaned_data.get('nohp')
		try:
			match = user.objects.get(nohp = nohp)
			self.add_error('nohp', "Nomor ini telah digunakan")
		except:
			return nohp

	def save(self, commit=True):
		userObj = super(UserRegisterForm, self).save(commit=False)
		userObj.set_password(userObj.password) # set password properly before commit
		if commit:
			userObj.save()
		return userObj