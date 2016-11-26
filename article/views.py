from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from category.models import ContentManagerCategory
from feedback.models import Comment, Like
from feedback.forms import CommentForm
from .models import Article, Category


class ArticleListView(ListView):
    model = Article

    def get_context_data(self, **kwargs):
        context = super(ArticleListView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class ArticleDetailView(DetailView):
    model = Article

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = \
            Comment.objects.filter(article_article=self.object)
        context['likes'] = len(Like.objects.filter(article=self.object))
        if self.request.user.is_authenticated():
            if len(Like.objects.filter(article=self.object,
                                       author=self.request.user)) != 0:
                context['liked'] = True
            else:
                context['liked'] = False
        else:
            context['liked'] = False
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
            categories = \
                ContentManagerCategory.objects.filter(
                    user=self.request.user).values("category")
            form.fields['category'].queryset = \
                Category.objects.filter(pk__in=categories)
        form.fields['title'].widget.attrs['class'] = 'form-control'
        form.fields['category'].widget.attrs['class'] = 'form-control'
        return form
