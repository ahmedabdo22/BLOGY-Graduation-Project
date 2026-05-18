from django.urls import path
from . import views

app_name = "publications"

urlpatterns = [
    path("", views.publications_view, name="publications_view"),
    path('create/',views.publication_create,name='publication_create'),
    path('details/<int:pk>/',views.publication_detail,name='publication_detail'),
    path('delete/<int:pk>/', views.publication_delete, name='publication_delete'),
]
