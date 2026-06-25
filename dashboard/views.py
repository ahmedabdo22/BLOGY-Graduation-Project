from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from accounts.signals import User , Profile
from articles.models import Article
from publications.models import Publication
from interactions.models import Clap
from django.db.models import Count, Sum, Q
from django.db.models.functions import Coalesce


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
def _users():
    users = User.objects.all()
    return users

def _total_articles():
    articles = Article.objects.all()
    return articles

def _total_publications():
    publications = Publication.objects.all()
    return publications

def _total_claps():
    claps = Clap.objects.values(
        'article__title',
        'article__publication__name',
        'article__slug',
        'article__status',
        'article__views_count',
        'user__username',
        'count'
    )
    return claps

def _top_author():
    top_authors = (
    User.objects
    .filter(profile__role='author')
    .annotate(
        total_articles=Count(
            'articles',
            filter=Q(articles__status='published')
        ),
        total_views=Coalesce(
            Sum('articles__views_count'),
            0
        ),
        total_claps=Count(
            'articles__claps',
            distinct=True
        )
    )
    .order_by(
        '-total_articles',
        '-total_claps',
        '-total_views',
    )[:1]
)
    return top_authors

def _top_publications():
    popular_publication = (
        Publication.objects
        .annotate(
            total_views=Coalesce(
                Sum('articles__views_count'),
                0
            )
        )
        .order_by('-total_views')
        .first()
    )
    return popular_publication

@staff_member_required
def admin_dashboard(request):
    users = _users().count()
    active_users = User.objects.filter(is_active=True).count()
    articles = _total_articles().count()
    #total of claps , views and get first 5 articles
    claps = _total_claps().order_by('-count', '-article__views_count')[:10]
    publications = _total_publications().count()
    total_views = _total_articles().filter(status = 'published').aggregate(sum=Sum('views_count'))['sum']
    total_claps = _total_claps().aggregate(sum=Sum('count'))['sum']
    top_author = _top_author()
    top_publication = _top_publications()
    print(total_views)
    return render(request , 'dashboard/admin_dashboard.html',
                  {
                   'total_users': users,
                   'active_users': active_users,
                   'total_articles': articles,
                   'total_publications': publications,
                   'claps': claps,
                   'total_views' : total_views,
                   'total_claps' : total_claps,
                   'top_author': top_author,
                   'top_publication': top_publication,
                   })

