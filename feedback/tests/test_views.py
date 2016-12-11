import json

from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.test import TestCase

from article.models import Article
from feedback.models import Comment, Like


class FeedbackViewsTestCase(TestCase):
    fixtures = ['feedback_views_testdata']

    def setUp(self):
        self.user = User.objects.all()[0]

    def test_comment(self):
        article = Article.objects.all()[0]

        url = reverse('feedback:comment', kwargs={'slug': article.slug})
        article_url = reverse('article:article-detail',
                              kwargs={'slug': article.slug})

        # should redirect to log in
        resp = self.client.get(url)
        self.assertRedirects(resp, reverse('login') + '?next=' + url)
        resp = self.client.post(url)
        self.assertRedirects(resp, reverse('login') + '?next=' + url)

        self.client.force_login(self.user)

        # should create comment only using POST
        resp = self.client.get(url)
        self.assertRedirects(resp, article_url)

        args = {
            'author': self.user.pk,
            'text': 'asd',
            'article': article.pk
        }
        self.client.post(url, args)

        comment = Comment.objects.latest('published')
        self.assertRedirects(resp, article_url)
        self.assertEqual(comment.author, self.user)
        self.assertEqual(comment.text, args['text'])
        self.assertEqual(comment.article_article, article)

    def test_reviewcomment(self):
        article = Article.objects.all()[0]

        comment = Comment.objects.create(author=self.user,
                                         text='a',
                                         article_article=article)
        url = reverse('feedback:review-comment',
                      kwargs={'comment_id': comment.pk})

        # should redirect to log in
        resp = self.client.get(url)
        self.assertRedirects(resp, reverse('admin:login') + '?next=' + url)
        resp = self.client.post(url)
        self.assertRedirects(resp, reverse('admin:login') + '?next=' + url)

        self.client.force_login(self.user)

        resp = self.client.get(url)
        self.assertRedirects(resp, '/')

        args = {
            'status': 'APP',
            'reviewer_comment': 'nice'
        }

        resp = self.client.post(url, args)
        comment = Comment.objects.get(pk=comment.pk)
        self.assertEqual(comment.status, args['status'])
        self.assertEqual(comment.reviewer_comment, args['reviewer_comment'])

    def test_like(self):
        article = Article.objects.all()[0]

        url = reverse('feedback:like', kwargs={'slug': article.slug})
        article_url = reverse('article:article-detail',
                              kwargs={'slug': article.slug})

        # should redirect to log in
        resp = self.client.get(url)
        self.assertRedirects(resp, reverse('login') + '?next=' + url)
        resp = self.client.post(url)
        self.assertRedirects(resp, reverse('login') + '?next=' + url)

        self.client.force_login(self.user)

        resp = self.client.get(url)
        self.assertRedirects(resp, article_url)

        resp = self.client.post(url)
        self.assertEqual(len(Like.objects.filter(article=article)), 1)

        resp = self.client.post(url)
        self.assertEqual(len(Like.objects.filter(article=article)), 0)

        resp = self.client.post(url, None,
                                HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        temp = json.loads(resp.content)
        self.assertEqual(temp['likes'], 1)

        resp = self.client.post(url, None,
                                HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        temp = json.loads(resp.content)
        self.assertEqual(temp['likes'], 0)
