from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
	def create_user(self, email, password=None, is_staff=False, is_admin= False, is_active = True):
		if not email:
			raise ValueError("Users must have email address")
		if not password:
			raise ValueError("Users must have password")

		user_obj = self.model(
			email = self.normalize_email(email)
		)
		user_obj.set_password(password)
		user_obj.staff = is_staff
		user_obj.admin = is_admin
		user_obj.active = is_active
		user_obj.save(using=self._db)
		return user_obj
	def create_staffuser(self,email, password=None):
		user = self.create_user(email, password=password, is_staff=True)
		return user
	def create_superuser(self,email, password=None):
		user = self.create_user(email, password=password, is_staff=True, is_admin=True)
		return user
