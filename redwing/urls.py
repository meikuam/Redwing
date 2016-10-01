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
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm

from news.forms import LoginForm

urlpatterns = [
	url(r'^', include('news.urls')),
	url(r'^admin/', admin.site.urls),
	url(r'^accounts/login/$', login, {'authentication_form': LoginForm}, name='login'),

	url(r'^accounts/logout/$', logout, {'next_page': '/'}, name='logout'),
	url(r'^accounts/register/$', CreateView.as_view(template_name='registration/register.html', form_class=UserCreationForm, success_url='/accounts/login/'))
]
