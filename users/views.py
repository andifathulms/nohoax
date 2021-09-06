from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from .forms import UserRegisterForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from .models import user
from django.core.mail import EmailMessage
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
# Create your views here.

def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			#form.save()
			userObj = form.save(commit=False)
			userObj.is_active = False
			userObj.save()
			
			#confirm_mail.apply_async((userObj.email, current_site), countdown=5)
			
			### Mail sender ###
			current_site = get_current_site(request)
			mail_subject = "Aktifasi akun anda"
			message = render_to_string('acc_active_email.html',{
				'user' : userObj,
				'domain' : current_site.domain,
				'uid': urlsafe_base64_encode(force_bytes(userObj.pk)),
				'token' : account_activation_token.make_token(userObj),
			})
			to_email = form.cleaned_data.get('email')
			email = EmailMessage(mail_subject, message, to=[to_email])
			email.send()
			return HttpResponse('Konfirmasi akun email anda')
			### End Mail Sender ###

			#username = form.cleaned_data.get('name')
			#messages.success(request, f'Account created for {username}!')
			return redirect('users-login')
	else:
		form = UserRegisterForm()
	return render(request, 'register.html', {'form':form})

def activate(request, uidb64, token):
	try:
		uid = force_text(urlsafe_base64_decode(uidb64))
		print(uid)
		userObj = user.objects.get(pk=uid)
		print(userObj)
	except(TypeError, ValueError, OverflowError, user.DoesNotExist):
		userObj = None
	if userObj is not None and account_activation_token.check_token(userObj, token):
		userObj.is_active = True
		userObj.save()
		login(request, userObj, backend='django.contrib.auth.backends.ModelBackend')
		#return redirect('home')
		return HttpResponse('Thank you for your email confirmation. Now you can login your account') 
	else:
		return HttpResponse('Activation link is invalid') #Change endpoint later

@login_required(login_url='users-login')
def profile(request):
	return render(request, 'profile.html', {})

class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter