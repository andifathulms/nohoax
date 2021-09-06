from rest_framework import parsers, renderers, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from users.models import user as User
from .serializers import RegistrationSerializer, CustomTokenSerializer
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from users.tokens import account_activation_token
from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created
from rest_framework.views import APIView

@api_view(['POST', ])
def registrationView(request):
	if request.method == 'POST':
		serializer = RegistrationSerializer(data=request.data)
		data = {}
		if serializer.is_valid():
			user = serializer.save()
			data['response'] = "Confirmation Pending"
			data['email'] = user.email
			data['name'] = user.name
			data['nohp'] = str(user.nohp)
			data['is_active'] = user.is_active
			data['is_staff'] = user.is_staff
			data['is_admin'] = user.is_admin
			token = Token.objects.get(user=user).key
			data['token'] = token

			#current_site = get_current_site(request)
			mail_subject = "Aktifasi akun anda"
			message = render_to_string('acc_active_email.html',{
				'user' : user,
				'domain' : "http://127.0.0.1:8000",
				'uid': urlsafe_base64_encode(force_bytes(user.pk)),
				'token' : account_activation_token.make_token(user),
			})
			
			to_email = user.email
			email = EmailMessage(mail_subject, message, to=[to_email])
			email.send()
			
		else:
			data = serializer.errors
		return Response(data)
