from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


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

class ContentManagerCategory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_staff': True})
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + ' can post to ' + self.category.name

    class Meta:
        verbose_name = "Content manager category"
        verbose_name_plural = "Content manager categories"
