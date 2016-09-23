from __future__ import unicode_literals

from django.db import models

from django.utils.encoding import python_2_unicode_compatible

from ckeditor.fields import RichTextField

@python_2_unicode_compatible
class Article(models.Model):
	title = models.CharField(max_length=200)
	content = RichTextField()
	published = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.title

	class Meta:
		ordering = ['-published']
