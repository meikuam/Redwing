from django.conf.urls import url

from . import views

app_name = 'news'
urlpatterns = [
	url(r'^$', views.ArticleListView.as_view(), name='article-list'),
	url(r'^article/(?P<slug>[-\w]+)/$', views.ArticleDetailView.as_view(), name='article-detail'),
        url(r'^article/(?P<slug>[-\w]+)/comment$', views.comment, name='comment')
]
