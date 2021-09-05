#obsolete
from django.core.mail import send_mail
from .models import user as User
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.shortcuts import get_object_or_404
from django.core.mail import EmailMessage

from celery import task
from .tokens import account_activation_token

@task
def confirm_mail(user_name, current_site):

    user_obj = get_object_or_404(User,username=user_name)
    token=account_activation_token.make_token(user_obj)

    subject = 'Aktifasi akun anda.'
    message = render_to_string(
        'acc_active_email.html',
        {
            'user': user_obj,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user_obj.pk)),
            'token': token,
        }
    )

    #to_email = form.cleaned_data.get('email')
    email = EmailMessage(mail_subject, message, to=[user_obj])
    email.send()
    return HttpResponse('Konfirmasi akun email anda')