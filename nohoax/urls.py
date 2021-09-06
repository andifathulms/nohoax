"""nohoax URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from main.views import home_view, index_view
from users.views import register, profile, activate, FacebookLogin
from users.api.views import registrationView
from rest_framework.authtoken.views import obtain_auth_token
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_view, name="main-index"),
    path('home/', home_view, name="main-home"),
    path('register/', register, name="users-register"),
    path('profile/', profile, name="users-profile"),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name="users-login"),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name="users-logout"),
    #path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', activate, name='activate')
    path('activate/<uidb64>/<token>', activate, name='activate'),
    path('api/register/', registrationView, name="api-register"),
    path('api/login/',obtain_auth_token,name="api-login"),
    path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='api-password_reset')), #obsolete
    path('dj-rest-auth/', include('dj_rest_auth.urls')), #obsolete
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')), #obsolete
    path('dj-rest-auth/facebook/', FacebookLogin.as_view(), name='fb_login'), #obsolete
]
