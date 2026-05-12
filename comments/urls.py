from django.urls import path
from . import views

app_name = "comments"

urlpatterns = [
    path("article/<slug:slug>/add/", views.add_comment, name="add"),
    path("<int:pk>/delete/", views.delete_comment, name="delete"),
]
