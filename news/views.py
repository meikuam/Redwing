from django.shortcuts import render, get_object_or_404, redirect

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .forms import CommentForm

from .models import Article, Comment

class ArticleListView(ListView):
	model = Article

class ArticleDetailView(DetailView):
	model = Article
	
	def get_context_data(self, **kwargs):
                context = super(ArticleDetailView, self).get_context_data(**kwargs)
                context['form'] = CommentForm()
                context['comments'] = Comment.objects.filter(news_article=self.object)
                return context

def comment(request, slug):
    article = get_object_or_404(Article, slug=slug)
    if request.method == 'POST': 
        form = CommentForm(request.POST)
    	if form.is_valid():
            comment = Comment(text=request.POST.get("text", ""), news_article=article)
            comment.save()
    return redirect(article, slug)

