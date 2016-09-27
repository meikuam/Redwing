from unidecode import unidecode
from django.template.defaultfilters import slugify

from django.db import models
from django.core.urlresolvers import reverse

from django.utils.encoding import python_2_unicode_compatible

from ckeditor.fields import RichTextField

from django.contrib.auth.models import User

class Category(models.Model):
        name = models.CharField(max_length=50)
        def __str__(self):
                return self.name

@python_2_unicode_compatible
class Article(models.Model):
	title = models.CharField(max_length=200)
	slug = models.SlugField(unique=True)
	content = RichTextField()
	published = models.DateTimeField(auto_now_add=True)
	author = models.ForeignKey(User, default=1)
	category = models.ForeignKey(Category)

	def __str__(self):
		return self.title

	class Meta:
		ordering = ['-published']

	def get_absolute_url(self):
		return reverse('news:article-detail', kwargs={'slug': self.slug})

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(unidecode(self.title))
		super(Article, self).save(*args, **kwargs)

class Comment(models.Model):
	author = models.ForeignKey(User, default=1)
	text = models.CharField(max_length=200)
	published = models.DateTimeField(auto_now_add=True)
	news_article = models.ForeignKey(Article)

	class Meta:
		ordering = ['-published']

