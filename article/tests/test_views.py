from django.core.urlresolvers import reverse
from django.test import TestCase, RequestFactory

from django.contrib.auth.models import User
from article.models import Article, Category
from article.views import ArticleCreateView


class ArticleViewsTestCase(TestCase):
    fixtures = ['article_views_testdata']

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.all()[0]

    def test_article_list(self):
        resp = self.client.get(reverse('article:article-list'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('object_list' in resp.context)
        self.assertTemplateUsed(resp, 'article/article_list.html')

    def test_article_detail(self):
        article = Article.objects.all()[0]
        resp = self.client.get(reverse('article:article-detail',
                               kwargs={'slug': article.slug}))

        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'article/article_detail.html')

        resp = self.client.get(reverse('article:article-detail',
                               kwargs={'slug': 'non-existent'}))
        self.assertEqual(resp.status_code, 404)

    def test_article_create(self):
        url = reverse('article:add-article')
        args = {
            'title': u'test',
            'content': u'test',
            'author': self.user,
            'category': Category.objects.all()[0]
        }

        resp = self.client.get(url)
        self.assertRedirects(resp, reverse('login') + '?next=' + url)

        resp = self.client.post(url, kwargs=args)
        self.assertRedirects(resp, reverse('login') + '?next=' + url)

        request = self.factory.get(url)
        request.user = self.user

        resp = ArticleCreateView.as_view()(request)
        self.assertEqual(resp.status_code, 200)

        request = self.factory.post(url, args)
        request.user = self.user

        resp = ArticleCreateView.as_view()(request)
        self.assertEqual(resp.status_code, 200)
