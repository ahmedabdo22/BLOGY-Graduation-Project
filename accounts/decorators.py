from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def role_required(allowed_roles=None):
    if allowed_roles is None:
        allowed_roles = ["author", "admin"]

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # Check if user has a profile and valid role
            if not hasattr(request.user, "profile") or request.user.profile.role not in allowed_roles:
                messages.error(request, "You are not allowed to access this page.")
                return redirect("publications:publications_view")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator