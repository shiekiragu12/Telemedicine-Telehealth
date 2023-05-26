from django.contrib import messages
from django.shortcuts import redirect


def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            messages.warning(request, 'You must be logged in as an admin')
            return redirect('index')
    return wrapper_func
