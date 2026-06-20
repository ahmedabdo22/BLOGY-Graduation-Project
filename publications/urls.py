from django.urls import path
from . import views

app_name = "publications"

urlpatterns = [
    path("", views.publications_view, name="publications_view"),
    path('create/',views.publication_create,name='publication_create'),
    path('details/<int:pk>/',views.publication_detail,name='publication_detail'),
    path('edit/<int:pk>/',views.publication_edit,name='publication_edit'),
    path('delete/<int:pk>/', views.publication_delete, name='publication_delete'),

    path("contributors/<int:pk>/", views.publication_contributors, name="publication_contributors"),
    path("invite/<int:pk>/", views.publication_invite, name="publication_invite"),
    path("invitation/<int:invite_id>/respond/", views.publication_invitation_respond,
         name="publication_invitation_respond"),
    path("invitations/", views.pending_invitations, name="pending_invitations"),
]
