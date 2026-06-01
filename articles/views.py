from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from .forms import ArticleForm
from .models import Article
from comments.forms import CommentForm
from comments.models import Comment
from django.db import models
from interactions.models import Bookmark, Clap

def article_list(request):
    articles = Article.objects.filter(status="published").select_related("author", "category")
    return render(request, "articles/article_list.html", {"articles": articles})

def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug, status="published")
    article.views_count += 1
    article.save(update_fields=["views_count"])
    comments = article.comments.filter(parent__isnull=True, is_active=True)
    comment_form = CommentForm()
    is_bookmarked = False
    user_claps = 0
    if request.user.is_authenticated:
        is_bookmarked = Bookmark.objects.filter(user=request.user, article=article).exists()
        clap = Clap.objects.filter(user=request.user, article=article).first()
        user_claps = clap.count if clap else 0
    return render(request, "articles/article_detail.html", {
        "article": article,
        "comments": comments,
        "comment_form": comment_form,
        "is_bookmarked": is_bookmarked,
        "user_claps": user_claps,
    })

@login_required
def article_create(request):
    from publications.models import Publication  # import here to avoid circular imports

    # Only show publications where the user is owner or contributor
    publications = Publication.objects.filter(
        models.Q(owner=request.user) |
        models.Q(contributors__user=request.user)
    ).distinct()

    form = ArticleForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        article = form.save(commit=False)
        article.author = request.user
        if article.status == "published":
            article.published_at = timezone.now()
        article.save()
        form.save_m2m()
        messages.success(request, "Article saved successfully.")
        return redirect(article.get_absolute_url() if article.status == "published" else "articles:my_articles")

    return render(request, "articles/article_form.html", {
        "form": form,
        "title": "Create Article",
        "publications": publications,
    })

@login_required
def article_edit(request, slug):
    from publications.models import Publication

    article = get_object_or_404(Article, slug=slug, author=request.user)
    publications = Publication.objects.filter(
        models.Q(owner=request.user) |
        models.Q(contributors__user=request.user)
    ).distinct()

    form = ArticleForm(request.POST or None, request.FILES or None, instance=article)
    if request.method == "POST" and form.is_valid():
        article = form.save(commit=False)
        if article.status == "published" and not article.published_at:
            article.published_at = timezone.now()
        article.save()
        form.save_m2m()
        messages.success(request, "Article updated successfully.")
        return redirect(article.get_absolute_url() if article.status == "published" else "articles:my_articles")

    return render(request, "articles/article_form.html", {
        "form": form,
        "title": "Edit Article",
        "publications": publications,
    })

@login_required
def article_delete(request, slug):
    article = get_object_or_404(Article, slug=slug, author=request.user)
    if request.method == "POST":
        article.delete()
        messages.success(request, "Article deleted successfully.")
        return redirect("articles:my_articles")
    return render(request, "articles/article_confirm_delete.html", {"article": article})

@login_required
def my_articles(request):
    articles = Article.objects.filter(author=request.user)
    return render(request, "articles/my_articles.html", {"articles": articles})
