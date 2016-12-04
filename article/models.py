from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.encoding import python_2_unicode_compatible
from unidecode import unidecode

from category.models import Category


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
        return reverse('article:article-detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.title))

        i = 1
        slug = self.slug
        while True:
            if not Article.objects.filter(slug=slug).exists():
                break
            i += 1
            slug = '%s-%d' % (self.slug, i)

        self.slug = slug
        super(Article, self).save(*args, **kwargs)
