from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect , get_object_or_404
from django.utils import timezone
from django.contrib import messages
from publications.forms import PublicationForm
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from .models import Publication, PublicationContributor, PublicationInvitation
from articles.models import Article
from accounts.decorators import role_required


# Create your views here.
@login_required
def publications_view(request):
    # Only fetch publications that are not already deleted
    qs = Publication.objects.all()
    return render(request,'publications/publications_list.html',{'qs' : qs})


@login_required
def publication_detail(request , pk):
    publication_object = get_object_or_404(Publication,pk=pk)
    articles = Article.objects.filter(publication=publication_object, status="published")
    return render(request, "publications/publication_detail.html",
                  {'publication' : publication_object,"articles": articles,})


@login_required
@role_required(["author", "admin"])
def publication_create(request):
    form = PublicationForm(request.POST or None, request.FILES or None )
    if form.is_valid():
        publication_data  = form.save(commit=False)
        publication_data.save()
        messages.success(request, "Publication Created")
        return redirect('publications:publications_view')
    else:
        form = PublicationForm()
    return render(request,'publications/create.html',{'form': form}
    )

@staff_member_required
def publication_delete(request, pk):
    # Only fetch publications that are not already deleted
    publication_object = get_object_or_404(Publication.objects.filter(delete_at__isnull=True),pk=pk)

    if request.method == "POST":
        publication_object.delete_at = timezone.now()  # mark as deleted
        publication_object.save()
        messages.success(request, "Publication Deleted")
        return redirect('publications:publications_view')

    return render(request,"publications/publication_delete_confirm.html",{"publication": publication_object}
    )

@staff_member_required
def publication_edit(request, pk):
    publication_object = get_object_or_404(Publication, pk=pk)
    users = User.objects.all()
    form = PublicationForm(request.POST or None, request.FILES or None, instance=publication_object)

    if request.method == "POST" and form.is_valid():
        publication = form.save(commit=False)

        # Handle restore checkbox
        if request.POST.get("restore") == "1":
            publication.delete_at = None  # restore by clearing delete_at

        publication.save()
        messages.success(request, "Publication Edited")
        return redirect('publications:publication_detail', pk=publication_object.pk)

    return render(
        request,
        "publications/publication_edit.html",
        {"form": form, "publication": publication_object, "users": users}
    )


@login_required
def publication_contributors(request, pk):
    publication = get_object_or_404(Publication, pk=pk)

    # ✅ Only allow owner or admin (staff)
    if request.user != publication.owner and not request.user.is_staff:
        messages.error(request, "You do not have permission to view members of this publication.")
        return redirect("publications:publications_view")

    contributors = PublicationContributor.objects.filter(publication=publication)
    pending_invites = PublicationInvitation.objects.filter(publication=publication, status="pending")

    return render(request, "publications/publication_contributors.html", {
        "publication": publication,
        "contributors": contributors,
        "pending_invites": pending_invites
    })

@login_required
def publication_invite(request, pk):
    publication = get_object_or_404(Publication, pk=pk)
    if request.method == "POST":
        invited_user_id = request.POST.get("invited_user")
        invited_user = get_object_or_404(User, pk=invited_user_id)

        PublicationInvitation.objects.create(
            publication=publication,
            invited_user=invited_user,
            invited_by=request.user,
            status="pending"
        )
        messages.success(request, f"Invitation sent to {invited_user.username}")
        return redirect("publications:publication_contributors", pk=pk)

    # ✅ exclude users already contributors
    users = User.objects.exclude(pk__in=publication.contributors.values_list("user_id", flat=True))
    return render(request, "publications/publication_invite.html", {
        "publication": publication,
        "users": users
    })


@login_required
def pending_invitations(request):
    invitations = PublicationInvitation.objects.filter(
        invited_user=request.user,
        status="pending"
    )
    return render(request, "publications/pending_invitations.html", {
        "invitations": invitations
    })

@login_required
def publication_invitation_respond(request, invite_id):
    invitation = get_object_or_404(PublicationInvitation, pk=invite_id)

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "accept":
            invitation.status = "accepted"
            invitation.save()
            PublicationContributor.objects.get_or_create(
                publication=invitation.publication,
                user=invitation.invited_user,
                role="writer"
            )
            messages.success(request, "You have joined the publication!")
        elif action == "reject":
            invitation.status = "rejected"
            invitation.save()
            messages.info(request, "Invitation rejected.")
        return redirect("publications:publications_view")

    return render(request, "publications/invitation_respond.html", {"invitation": invitation})

