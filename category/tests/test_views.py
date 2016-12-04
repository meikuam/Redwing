from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test import Client
from category.models import Category


class CategoriesTestCase(TestCase):
    def test_categories(self):
        c = Client()
        cat = Category.objects.create(name="test_category")
        response = c.get(reverse('category:category',
                         kwargs={'category_id': cat.id}))
        self.assertEquals(response.status_code, 200)
        self.assertTrue(cat in response.context['categories'])
        response = c.get(reverse('category:category',
                         kwargs={'category_id': 10}))
        self.assertEquals(response.status_code, 404)
