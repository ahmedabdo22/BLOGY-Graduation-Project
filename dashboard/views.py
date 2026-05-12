from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from articles.models import Article

@login_required
def author_dashboard(request):
    articles = Article.objects.filter(author=request.user)
    total_views = sum(a.views_count for a in articles)
    total_claps = sum(sum(c.count for c in a.claps.all()) for a in articles)
    return render(request, "dashboard/author_dashboard.html", {
        "articles": articles,
        "total_views": total_views,
        "total_claps": total_claps,
    })
