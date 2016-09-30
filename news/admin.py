from django.contrib import admin

from .models import Article, Comment, Category, ContentManagerCategory

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
	exclude = ('slug', 'author')

admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(ContentManagerCategory)

