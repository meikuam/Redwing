from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import UserPassesTestMixin

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from .forms import CommentForm

from .models import Article, Comment, Category

from django.contrib.auth.decorators import login_required


class ArticleListView(ListView):
	model = Article
	def get_context_data(self, **kwargs):
		context = super(ArticleListView, self).get_context_data(**kwargs)
		context['categories'] =  Category.objects.all()
		return context

class ArticleDetailView(DetailView):
	model = Article
	def get_context_data(self, **kwargs):
		context = super(ArticleDetailView, self).get_context_data(**kwargs)
		context['form'] = CommentForm()
		context['comments'] = Comment.objects.filter(news_article=self.object)
		return context

class ArticleCreateView(UserPassesTestMixin, CreateView):
	model = Article
	fields = ['title', 'content']
	template_name_suffix = '_create_form'

	def test_func(self):
		return self.request.user.is_staff

@login_required(redirect_field_name=None, login_url='/accounts/login/')
def comment(request, slug):
	article = get_object_or_404(Article, slug=slug)
	if request.method == 'POST': 
		form = CommentForm(request.POST)
		if form.is_valid():
			comment = Comment(author=request.user, text=request.POST.get("text", ""), news_article=article)
			comment.save()
	return redirect(article, slug)

def category(request, category_id):
	categories = Category.objects.all()
	category = get_object_or_404(Category, pk=category_id)
	article_list_by_category = Article.objects.filter(category=category)
	context = { 'object_list': article_list_by_category, 'categories': categories }
	print article_list_by_category
	return render(request, 'news/article_list.html', context)
