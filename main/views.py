from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.

context = {'title': 'No Hoax'}
@login_required(login_url='users-login')
def home_view(request, *args, **kwargs):
	return render(request, "home.html", context)

def index_view(request, *args, **kwargs):
	return render(request, "index.html", context)
