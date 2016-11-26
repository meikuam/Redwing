from django.conf.urls import url

from . import views


app_name = 'feedback'
urlpatterns = [
    url(r'^article/(?P<slug>[-\w]+)/comment$',
        views.comment,
        name='comment'),
    url(r'^reviewcomment/(?P<comment_id>[0-9]+)/$',
        views.reviewcomment,
        name='review-comment'),
    url(r'^article/(?P<slug>[-\w]+)/like$',
        views.like,
        name='like'),
]
