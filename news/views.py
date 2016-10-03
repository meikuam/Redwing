from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import UserPassesTestMixin

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from django import forms
from .forms import CommentForm, CommentReviewForm

from .models import Article, Comment, Category, ContentManagerCategory, Like

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
		context['likes'] = len(Like.objects.filter(article=self.object))
		context['liked'] = 'True' if len(Like.objects.filter(article=self.object, author=self.request.user)) != 0 else 'False'
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

	def get_form(self, **kwargs):
		form = super(ArticleCreateView, self).get_form(**kwargs)
		if not self.request.user.is_superuser:
			categories = ContentManagerCategory.objects.filter(user=self.request.user).values("category")
			form.fields['category'].queryset = Category.objects.filter(pk__in=categories)

		form.fields['title'].widget.attrs['class'] = 'form-control'
		form.fields['category'].widget.attrs['class'] = 'form-control'
		return form

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
	return render(request, 'news/article_list.html', context)

@staff_member_required
def reviewcomment(request, comment_id):
	comment = get_object_or_404(Comment, pk=comment_id)
	if request.method == 'POST': 
		form = CommentReviewForm(request.POST)
		if form.is_valid():
			comment.status = request.POST['status']
			comment.reviewer_comment = request.POST['reviewer_comment']
			comment.save()
	return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required(redirect_field_name=None, login_url='/accounts/login/')
def like(request, slug):
	article = get_object_or_404(Article, slug=slug)
	if request.method == 'POST':
		like_ = Like.objects.filter(article=article, author=request.user)
		if len(like_) == 0:
			like_ = Like(article=article, author=request.user)
			like_.save()
		else:
			like_.delete()
	return redirect(article, slug)
