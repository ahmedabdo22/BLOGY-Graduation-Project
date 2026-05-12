from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from articles.models import Article
from .forms import CommentForm
from .models import Comment

@login_required
def add_comment(request, slug):
    article = get_object_or_404(Article, slug=slug)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.article = article
        comment.user = request.user
        parent_id = request.POST.get("parent_id")
        if parent_id:
            comment.parent = Comment.objects.filter(id=parent_id, article=article).first()
        comment.save()
        messages.success(request, "Comment added successfully.")
    else:
        messages.error(request, "Comment cannot be empty.")
    return redirect(article.get_absolute_url())

@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk, user=request.user)
    article = comment.article
    comment.delete()
    messages.success(request, "Comment deleted successfully.")
    return redirect(article.get_absolute_url())
