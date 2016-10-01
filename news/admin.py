from django.contrib import admin

from .models import Comment, Category, ContentManagerCategory

admin.site.register(Category)
admin.site.register(ContentManagerCategory)

