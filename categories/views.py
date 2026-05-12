from django.shortcuts import get_object_or_404, render
from .models import Category, Tag

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    articles = category.articles.filter(status="published")
    return render(request, "categories/category_detail.html", {"category": category, "articles": articles})

def tag_detail(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    articles = tag.articles.filter(status="published")
    return render(request, "categories/tag_detail.html", {"tag": tag, "articles": articles})
