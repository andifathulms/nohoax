from django.shortcuts import render

# Create your views here.

context = {'title': 'No Hoax'}
def home_view(request, *args, **kwargs):
	return render(request, "index.html", context)
