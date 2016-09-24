from django.conf.urls import url

from . import views

app_name = 'news'
urlpatterns = [
	url(r'^$', views.ArticleListView.as_view(), name='article-list'),
	url(r'^article/(?P<pk>[0-9]+)/$', views.ArticleDetailView.as_view(), name='article-detail')
]