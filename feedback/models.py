from django.contrib.auth.models import User
from django.db import models

from article.models import Article


class Comment(models.Model):
    author = models.ForeignKey(User, default=1)
    text = models.CharField(max_length=200)
    published = models.DateTimeField(auto_now_add=True)
    news_article = models.ForeignKey(Article)
    reviewer_comment = models.CharField(max_length=200, blank=True, null=True)
    reviewer = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='comment_reviewer')
    NEW = 'NEW'
    APPROVED = 'APP'
    REJECTED = 'REJ'
    COMMENT_STATUSES = (
        (NEW, 'New'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
    )
    status = models.CharField(max_length=3, choices=COMMENT_STATUSES, default=NEW)

    class Meta:
        ordering = ['-published']


class Like(models.Model):
    article = models.ForeignKey(Article)
    author = models.ForeignKey(User)
    published = models.DateTimeField(auto_now_add=True)
