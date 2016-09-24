from django.shortcuts import render

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Article

class ArticleListView(ListView):
	model = Article

class ArticleDetailView(DetailView):
	model = Article
