from __future__ import unicode_literals

from django.db import models


class User(models.Model):
    login = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    username = models.CharField(max_length=20)


class Category(models.Model):
    name = models.CharField(max_length=50)


class NewsArticle(models.Model):
    title = models.CharField(max_length=50)
    text = models.TextField()
    date = models.DateTimeField('Date published')
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    text = models.TextField()
    date = models.DateTimeField('Date published')
    rejection_comment = models.CharField(max_length=200)
    author = models.ForeignKey(User, null=True, 
        on_delete=models.SET_NULL, 
        related_name='comment_author')
    reviewer = models.ForeignKey(User, null=True, 
        on_delete=models.SET_NULL, 
        related_name='comment_reviewer')
    news_article = models.ForeignKey(NewsArticle, on_delete=models.CASCADE)
    NEW = 'NEW'
    APPROVED = 'APP'
    REJECTED = 'REJ'
    COMMENT_STATUSES = (
        (NEW, 'New'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
    )
    status = models.CharField(max_length=3, 
        choices=COMMENT_STATUSES, default=NEW)


class Like(models.Model):
    date = models.DateTimeField('Date published')
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)


class ContentManagerCategories(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
