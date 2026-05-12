from django.urls import path
from . import views

app_name = "articles"

urlpatterns = [
    path("", views.article_list, name="list"),
    path("mine/", views.my_articles, name="my_articles"),
    path("create/", views.article_create, name="create"),
    path("<slug:slug>/", views.article_detail, name="detail"),
    path("<slug:slug>/edit/", views.article_edit, name="edit"),
    path("<slug:slug>/delete/", views.article_delete, name="delete"),
]
