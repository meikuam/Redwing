from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .forms import CommentForm, ArticleForm

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

@user_passes_test(lambda user: user.is_staff)
def add_article(request):
	if request.method == 'POST':
		form = ArticleForm(request.POST)

		if form.is_valid():
			article = Article(title=request.POST['title'], content=request.POST['content'], author=request.user)
			article.save()

			return redirect(article, article.slug)

	else:
		form = ArticleForm()

	return render(request, 'news/add_article.html', {'form': form})
