from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from .forms import CommentForm, CommentReviewForm
from article.models import Article
from feedback.models import Comment, Like



@login_required(login_url='/accounts/login/')
def comment(request, slug):
    article = get_object_or_404(Article, slug=slug)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(author=request.user, text=request.POST.get("text", ""), article_article=article)
            if request.user.is_staff:
                comment.status = "APP"
            comment.save()
    return redirect(article, slug)



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



@login_required(login_url='/accounts/login/')
def like(request, slug):
    article = get_object_or_404(Article, slug=slug)
    if request.method == 'POST':
        like_ = Like.objects.filter(article=article, author=request.user)
        if len(like_) == 0:
            like_ = Like(article=article, author=request.user)
            like_.save()
        else:
            like_.delete()

    if request.is_ajax():
        resp = {"likes": str(len(Like.objects.filter(article=article)))}
        return JsonResponse(resp)
    return redirect(article, slug)
