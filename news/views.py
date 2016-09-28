from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import UserPassesTestMixin

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from .forms import CommentForm, CommentReviewForm

from .models import Article, Comment, Category

from django.contrib.auth.decorators import login_required

from django.http import HttpResponseRedirect

from django.contrib.admin.views.decorators import staff_member_required


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
	fields = ['title', 'category', 'content']
	template_name_suffix = '_create_form'

	def test_func(self):
		return self.request.user.is_staff

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super(ArticleCreateView, self).form_valid(form)

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

@staff_member_required
def reviewcomment(request, comment_id):
	comment = get_object_or_404(Comment, pk=comment_id)
	if request.method == 'POST': 
		form = CommentReviewForm(request.POST)
		print request.POST['status']
		print request.POST['reviewer_comment']
		if form.is_valid():
			print "yes its valid"
			comment.status = request.POST['status']
			comment.reviewer_comment = request.POST['reviewer_comment']
			comment.save()
	return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


