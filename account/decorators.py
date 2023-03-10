from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.warning(request, 'You are already logged In')
            return redirect('index')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func


def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('index')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func
