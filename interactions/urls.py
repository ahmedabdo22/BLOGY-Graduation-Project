from django.urls import path
from . import views

app_name = "interactions"

urlpatterns = [
    path("bookmarks/", views.bookmarks, name="bookmarks"),
    path("article/<slug:slug>/clap/", views.clap_article, name="clap"),
    path("article/<slug:slug>/bookmark/", views.toggle_bookmark, name="bookmark"),
    path("article/<slug:slug>/report/", views.report_article, name="report"),
    path("follow/<str:username>/", views.toggle_follow, name="follow"),
]
