from django.core.urlresolvers import reverse
from django.test import TestCase, RequestFactory

from django.contrib.auth.models import User
from article.models import Article, Category


class ArticleViewsTestCase(TestCase):
    fixtures = ['article_views_testdata']

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.all()[0]

    def test_article_list(self):
        articles = Article.objects.all()

        resp = self.client.get(reverse('article:article-list'))

        self.assertEqual(resp.status_code, 200)
        self.assertTrue('object_list' in resp.context)
        self.assertTrue(
            article in resp.context['object_list'] for article in articles
        )
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
        user = self.user
        category = Category.objects.all()[0]
        args = {
            'title': u'test-title',
            'content': u'test',
            'author': user.pk,
            'category': category.pk
        }

        resp = self.client.get(url)
        self.assertRedirects(resp, reverse('login') + '?next=' + url)

        resp = self.client.post(url, kwargs=args)
        self.assertRedirects(resp, reverse('login') + '?next=' + url)

        self.client.force_login(user)

        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

        resp = self.client.post(url, args)
        article = Article.objects.latest('published')

        self.assertRedirects(resp, reverse('article:article-detail',
                             kwargs={'slug': article.slug}))
        self.assertEqual(article.title, args['title'])
        self.assertEqual(article.content, args['content'])
        self.assertEqual(article.author, user)
        self.assertEqual(article.category, category)
