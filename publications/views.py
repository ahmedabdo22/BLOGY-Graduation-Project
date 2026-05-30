from django.shortcuts import render, redirect , get_object_or_404
from django.utils import timezone
from .models import Publication
from django.contrib import messages
from publications.forms import PublicationForm
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User




# Create your views here.
@staff_member_required
def publications_view(request):
    # Only fetch publications that are not already deleted
    qs = Publication.objects.all()
    return render(request,'publications/publications_list.html',{'qs' : qs})


@staff_member_required
def publication_detail(request , pk):
    publication_object = get_object_or_404(Publication,pk=pk)
    return render(request, "publications/publication_detail.html",{'publication' : publication_object})


@staff_member_required
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