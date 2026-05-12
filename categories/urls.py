from django.urls import path
from . import views

app_name = "categories"

urlpatterns = [
    path("category/<slug:slug>/", views.category_detail, name="category_detail"),
    path("tag/<slug:slug>/", views.tag_detail, name="tag_detail"),
]
