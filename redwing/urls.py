"""redwing URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import login, logout

from auth.views import register
from auth.forms import LoginForm


urlpatterns = [
    url(r'^', include('article.urls')),
    url(r'^', include('category.urls')),
    url(r'^', include('feedback.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/login/$', login,
        {'authentication_form': LoginForm,
        'redirect_authenticated_user': True},
        name='login'),
    url(r'^accounts/logout/$', logout,
        {'next_page': '/'},
        name='logout'),
    url(r'^accounts/register/$', register,
        name='register'),
]
