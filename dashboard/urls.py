from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.author_dashboard, name="author_dashboard"),
    path("admin-Dashboard",views.admin_dashboard, name="admin_dashboard"),

]
