from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from articles.models import Article
from .forms import ReportForm
from .models import Bookmark, Clap, Follow, Report

@login_required
def clap_article(request, slug):
    article = get_object_or_404(Article, slug=slug)
    clap, created = Clap.objects.get_or_create(user=request.user, article=article)
    if not created:
        clap.count += 1
        clap.save()
    messages.success(request, "Thanks for clapping.")
    return redirect(article.get_absolute_url())

@login_required
def toggle_bookmark(request, slug):
    article = get_object_or_404(Article, slug=slug)
    bookmark, created = Bookmark.objects.get_or_create(user=request.user, article=article)
    if not created:
        bookmark.delete()
        messages.info(request, "Removed from bookmarks.")
    else:
        messages.success(request, "Added to bookmarks.")
    return redirect(article.get_absolute_url())

@login_required
def bookmarks(request):
    items = Bookmark.objects.filter(user=request.user).select_related("article")
    return render(request, "interactions/bookmarks.html", {"items": items})

@login_required
def toggle_follow(request, username):
    from django.contrib.auth.models import User
    target = get_object_or_404(User, username=username)
    if target == request.user:
        messages.error(request, "You cannot follow yourself.")
        return redirect("accounts:public_profile", username=username)
    follow, created = Follow.objects.get_or_create(follower=request.user, following=target)
    if not created:
        follow.delete()
        messages.info(request, "Unfollowed user.")
    else:
        messages.success(request, "Followed user.")
    return redirect("accounts:public_profile", username=username)

@login_required
def report_article(request, slug):
    article = get_object_or_404(Article, slug=slug)
    form = ReportForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        report = form.save(commit=False)
        report.article = article
        report.reporter = request.user
        report.save()
        messages.success(request, "Report submitted for admin review.")
        return redirect(article.get_absolute_url())
    return render(request, "interactions/report_form.html", {"form": form, "article": article})
