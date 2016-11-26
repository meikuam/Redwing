from django.conf.urls import url

from . import views


app_name = 'category'
urlpatterns = [
     url(r'^category/(?P<category_id>[0-9]+)/$',
         views.category,
         name='category'),
]
