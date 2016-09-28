from django.contrib import admin

from .models import Article
from .models import Comment
from .models import Category

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
	exclude = ('slug', 'author')

	def save_model(self, request, obj, form, change):
		if getattr(obj, 'author', None) is None:
			obj.author = request.user
		obj.save()

admin.site.register(Comment)
admin.site.register(Category)

