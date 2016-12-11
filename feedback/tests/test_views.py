from django.core.urlresolvers import reverse
from django.test import TestCase, RequestFactory
from article.models import Article
from feedback.models import Comment, Like
from feedback.views import comment, reviewcomment, like
from category.models import Category
from django.contrib.auth.models import User

class FeedbackViewsTestCase(TestCase):


    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.all()[0]
        self.category = Category.objects.create(name=u'Sport')
        self.article = Article.objects.create(
            title=u'test',
            content=u'test',
            author=self.user,
            category=self.category
        )

    def test_comment_add(self):
        url = reverse('article:comment')
        args = {
            'author': self.user,
            'text': u'test',
            'article_article': self.article
        }

        resp = self.client.get(url)
        self.assertRedirects(resp, reverse('login') + '?next=' + url)

        request = self.factory.get(url)
        request.user = self.user

        resp = comment()(request)
        self.assertEqual(resp.status_code, 200)


