from unidecode import unidecode
from django.template.defaultfilters import slugify

from django.db import models
from django.core.urlresolvers import reverse

from django.utils.encoding import python_2_unicode_compatible

from ckeditor.fields import RichTextField

from django.contrib.auth.models import User

@python_2_unicode_compatible
class Category(models.Model):
	name = models.CharField(max_length=50)
	
	def __str__(self):
		return self.name
		
	def get_absolute_url(self):
		return reverse('news:category', kwargs={'category_id': self.id})
		
	class Meta:
		verbose_name = "Category"
		verbose_name_plural = "Categories"

@python_2_unicode_compatible
class Article(models.Model):
	title = models.CharField(max_length=200)
	slug = models.SlugField(unique=True)
	content = RichTextField()
	published = models.DateTimeField(auto_now_add=True)
	author = models.ForeignKey(User)
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
	reviewer_comment = models.CharField(max_length=200, blank=True, null=True)
	reviewer = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='comment_reviewer')
	NEW = 'NEW'
	APPROVED = 'APP'
	REJECTED = 'REJ'
	COMMENT_STATUSES = (
		(NEW, 'New'),
		(APPROVED, 'Approved'),
		(REJECTED, 'Rejected'),
	)
	status = models.CharField(max_length = 3, choices=COMMENT_STATUSES, default=NEW)

	class Meta:
		ordering = ['-published']


class ContentManagerCategory(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_staff': True})
	category = models.ForeignKey(Category, on_delete=models.CASCADE)

	def __str__(self):
		return self.user.username + ' can post to ' + self.category.name

	class Meta:
		verbose_name = "Content manager category"
		verbose_name_plural = "Content manager categories"



class Like(models.Model):
	article = models.ForeignKey(Article)
	author = models.ForeignKey(User)
	time_stamp = models.DateTimeField(auto_now_add=True)
