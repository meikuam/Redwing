from django.contrib import admin

from .models import Article
from .models import Comment

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
	exclude = ('slug', 'author')

admin.site.register(Comment)
