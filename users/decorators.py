from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


def role_required(*roles):
    def decorator(view_func):
        @login_required
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            profile = getattr(request.user, "userprofile", None)
            if not profile or profile.role not in roles:
                messages.error(request, "You do not have permission to access that page.")
                return redirect("dashboard")
            if not profile.is_approved and profile.role not in {"student", "admin"}:
                messages.warning(request, "Your account is awaiting approval.")
                return redirect("dashboard")
            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator
