from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect , get_object_or_404
from .models import Publication
from django.contrib import messages
from publications.forms import PublicationForm



# Create your views here.
def publications_view(request):
    qs = Publication.objects.filter( delete_at__isnull=True)
    return render(request,'publications/publications_list.html',{'qs' : qs})



def publication_detail(request , pk):
    publication_object = get_object_or_404(Publication.objects.filter(delete_at__isnull=True),pk=pk)
    print(publication_object)
    return render(request, "publications/publication_detail.html",{'publication' : publication_object})


@login_required
def publication_create(request):
    form = PublicationForm(request.POST or None, request.FILES or None )
    if form.is_valid():
        publication_data  = form.save(commit=False)
        publication_data.owner = request.user
        publication_data.save()
        messages.success(request, "Publication Created")
        qs = Publication.objects.filter( delete_at__isnull=True)
        return render(request,'publications/publications_list.html',{'qs' : qs})
    else:
        form = PublicationForm()
    return render(request,'publications/create.html',{'form': form}
    )

@login_required
def publication_delete(request, pk):
    publication_object = get_object_or_404(Publication.objects.filter(delete_at__isnull=True), pk=pk)
    if request.method == "POST":
        publication_object.delete()
        messages.success(request, "Publication Deleted")
        return redirect('publications_list')
    return render(request,'publications/publication_detail.html',{'publication' : publication_object})