from django.urls import path
from . import views

app_name = "moderation"

urlpatterns = [
    path("", views.moderation_dashboard, name="dashboard"),
    path("all-users", views.all_users, name="all_users"),
    path("users/<int:user_id>/",views.user_profile_detail,name="user_profile_detail"),
    path("articles/",views.article_view_admin,name="article_view_admin"),
    path("article_details/<int:pk>/",views.article_details,name="article_details"),
    path("test/",views.test,name="test"),
]

