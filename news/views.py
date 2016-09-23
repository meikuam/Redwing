from django.shortcuts import render

from django.views.generic.list import ListView

from .models import Article

class ArticleListView(ListView):
	model = Article
