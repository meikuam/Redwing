from django.test import TestCase

from django.contrib.auth.models import User
from article.models import Article, Category


class ArticleModelTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name=u'Sports')
        self.user = User.objects.create(username=u'test', password=u'secret')

    def test_save(self):
        new_article = Article.objects.create(
            title=u'test',
            content=u'test',
            author=self.user,
            category=self.category
        )

        self.assertEqual(new_article.title, u'test')
        self.assertEqual(new_article.content, u'test')
        self.assertEqual(new_article.author, self.user)
        self.assertEqual(new_article.category, self.category)

    def test_unique_slug(self):
        new_article1 = Article.objects.create(
            title=u'test',
            content=u'test',
            author=self.user,
            category=self.category
        )

        new_article2 = Article.objects.create(
            title=u'test',
            content=u'test',
            author=self.user,
            category=self.category
        )

        self.assertTrue(new_article1.slug != new_article2.slug)
