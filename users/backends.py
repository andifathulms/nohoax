from django.contrib.auth.backends import ModelBackend
from .models import user

class EmailAuthBackend(ModelBackend):
	def authenticate(self, request, username=None, password=None):
		try:
			userObj = user.objects.get(email=username)
			print(userObj.password)
			print(password)
			if userObj.check_password(password):
				return userObj
		except user.DoesNotExist:
			user().set_password(password)