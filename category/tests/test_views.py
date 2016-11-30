from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test import Client
from category.models import Category


class RegisterTestCase(TestCase):
    def test_categories(self):
        c = Client()
        Category.objects.create(name="test_category")
        cat = Category.objects.all()[0]
        response = c.get(reverse('category:category',
                         kwargs={'category_id': cat.id}))
        self.assertEquals(response.status_code, 200)
        response = c.get(reverse('category:category',
                         kwargs={'category_id': 10}))
        self.assertEquals(response.status_code, 404)
