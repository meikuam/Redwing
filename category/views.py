from django.shortcuts import render, get_object_or_404
from .models import Category
from article.models import Article


def category(request, category_id):
    categories = Category.objects.all()
    category = get_object_or_404(Category, pk=category_id)
    article_list_by_category = Article.objects.filter(category=category)
    context = {'object_list': article_list_by_category, 'categories': categories}
    return render(request, 'templates/article/article_list.html', context)


