from functools import wraps
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from .models import Publication

def publication_owner_or_admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, slug, *args, **kwargs):
        publication = get_object_or_404(Publication, slug=slug)

        # Check ownership or admin privileges
        if not (
            request.user == publication.owner
            or request.user.is_staff
            or request.user.is_superuser
        ):
            messages.error(request, "You are not allowed to perform this action.")
            return redirect("publications:publication_detail", slug=publication.slug)

        return view_func(request, slug, *args, **kwargs)

    return _wrapped_view
