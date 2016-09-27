from django.contrib import admin

from .models import Article
from .models import Comment
from .models import Category

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
	exclude = ('slug', 'author')

admin.site.register(Comment)
admin.site.register(Category)

