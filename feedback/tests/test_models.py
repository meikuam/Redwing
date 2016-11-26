import datetime
from django.test import TestCase
from django.contrib.auth.models import User, AnonymousUser
from feedback.models import Comment, Like
from article.models import Category, Article


class FeedbackTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(username=u'test',
                                        password=u'secret')
        self.category = Category.objects.create(name=u'Sport')
        self.article = Article.objects.create(
            title=u'test',
            content=u'test',
            author=self.user,
            category=self.category
        )

    def test_comment_add(self):
        """Comment add test"""
        comment = Comment.objects.create(author=self.user,
                                         text=u'text',
                                         article_article=self.article)
        self.assertEqual(comment.author, self.user)
        self.assertEqual(comment.article_article, self.article)

    def test_like_by_anonymous(self):
        with self.assertRaises(ValueError):
            like = Like.objects.create(article=self.article,
                                       author=AnonymousUser)

    def test_add_like(self):
        like = Like.objects.create(article=self.article,
                                   author=self.user)
        self.assertEqual(like.article, self.article)
        self.assertEqual(like.author, self.user)
