from django.contrib.admin.views.decorators import staff_member_required
from interactions.models import Report
from django.contrib.auth.models import User
from django.db.models import Sum , Count
from django.shortcuts import get_object_or_404, render
from articles.models import Article
from publications.models import Publication


@staff_member_required
def moderation_dashboard(request):
    reports = Report.objects.select_related("article", "reporter").order_by("-created_at")
    return render(request, "moderation/moderation_dashboard.html", {"reports": reports})



@staff_member_required
def all_users(request):
    users = User.objects.annotate(article_count=Count('articles')
            ).values(
                'id',
                'username',
                'is_active',
                'profile__role',
                'article_count'
            ).order_by('id')
    return render(request, 'moderation/all_users.html', {
        'all_users': users,
    })

@staff_member_required
def user_profile_detail(request, user_id):
    #user = get_object_or_404(User.objects.filter(pk=user_id).select_related("profile"))
    user= User.objects.select_related("profile").get(pk=user_id)

    articles = (Article.objects.filter(author=user).order_by("-created_at"))

    published_articles = articles.filter(status="published")

    total_views = (published_articles.aggregate(total=Sum("views_count"))["total"] or 0)

    total_claps = (published_articles.aggregate(total=Count("claps"))["total"] or 0)

    total_reports = (articles.annotate(report_count=Count("reports")).aggregate(total=Sum("report_count"))["total"] or 0)

    context = {
        "profile_user": user,
        "profile": user.profile,
        "articles": articles[:10],
        "articles_count": articles.count(),
        "published_count": articles.filter(status="published").count(),
        "draft_count": articles.filter(status="draft").count(),
        "total_views": total_views,
        "total_claps": total_claps,
        "total_reports": total_reports,
        "is_active": user.is_active,
        "date_joined": user.date_joined,
        "last_login": user.last_login,
    }

    return render(
        request,
        "moderation/user_profile_detail.html",
        context
    )




@staff_member_required
def article_view_admin(request):

    articles = (Article.objects.all().prefetch_related("claps","comments","reports").order_by("-created_at"))
    # Statistics
    total_articles = Article.objects.count()
    published_articles = Article.objects.filter(status="published").count()
    draft_articles = Article.objects.filter(status="draft").count()
    reported_articles = Report.objects.count()

    context = {
        "articles": articles,
        "total_articles": total_articles,
        "published_articles": published_articles,
        "draft_articles": draft_articles,
        "reported_articles": reported_articles,
    }

    return render(
        request,
        "moderation/article_view_admin.html",
        context,
    )
@staff_member_required
def article_details(request , pk):
    article = Article.objects.prefetch_related("claps","comments","reports").get(pk=pk)
    return render(request, "moderation/article_details.html",{"article": article})

def test(request):
    #QS = Article.objects.all().prefetch_related("claps","comments","reports")
    QS = Publication.objects.all().prefetch_related("articles")
    BB = User.objects.annotate(TT=Count('articles'))
    Test = Publication.objects.prefetch_related("articles").get(pk=27)

    print(BB)
    return render(request, "moderation/test.html",{"QS":QS , "Test":Test , "BB":BB})