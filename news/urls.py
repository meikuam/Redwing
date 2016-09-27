from django.conf.urls import url
from django.contrib.auth.views import login
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm

from . import views

app_name = 'news'
urlpatterns = [
	url(r'^$', views.ArticleListView.as_view(), name='article-list'),
	url(r'^article/(?P<slug>[-\w]+)/$', views.ArticleDetailView.as_view(), name='article-detail'),
	url(r'^article/(?P<slug>[-\w]+)/comment$', views.comment, name='comment'),
	url(r'^addarticle/?$', views.ArticleCreateView.as_view(), name='add-article'),
	url(r'^category/(?P<category_id>[0-9]+)/$', views.category, name='category'),
    url(r'^accounts/login/$', login, name='login'),
    url(r'^accounts/register/$', CreateView.as_view(template_name='registration/register.html', form_class=UserCreationForm, success_url='/accounts/login/'))
]
