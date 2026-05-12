from django.db.models import Q
from django.shortcuts import render
from articles.models import Article
from categories.models import Category, Tag

def home(request):
    articles = Article.objects.filter(status="published").select_related("author", "category")
    categories = Category.objects.all()
    tags = Tag.objects.all()

    query = request.GET.get("q", "")
    category = request.GET.get("category", "")
    tag = request.GET.get("tag", "")

    if query:
        articles = articles.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(author__username__icontains=query)
        )
    if category:
        articles = articles.filter(category__slug=category)
    if tag:
        articles = articles.filter(tags__slug=tag)

    return render(request, "core/home.html", {
        "articles": articles,
        "categories": categories,
        "tags": tags,
        "query": query,
    })

def about(request):
    return render(request, "core/about.html")
