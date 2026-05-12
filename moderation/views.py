from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from interactions.models import Report

@staff_member_required
def moderation_dashboard(request):
    reports = Report.objects.select_related("article", "reporter").order_by("-created_at")
    return render(request, "moderation/moderation_dashboard.html", {"reports": reports})
