from django.test import TestCase
from django.contrib.auth.models import User
from category.models import Category, ContentManagerCategory


class RegisterTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name=u'Sports')
        self.user = User.objects.create(username=u'test', password=u'secret')

    def test_categories(self):
        name = "test_cat1"
        cat = Category.objects.create(name=name)
        print cat.__str__()
        self.assertEquals(cat.__str__(), 'test_cat1')
        self.assertEquals(cat.get_absolute_url(),
                          '/category/' + str(cat.id) + '/')

    def test_cm_categories(self):
        cmc = ContentManagerCategory.objects.create(user=self.user,
                                                    category=self.category)
        self.assertEquals(cmc.__str__(), 'test can post to Sports')
