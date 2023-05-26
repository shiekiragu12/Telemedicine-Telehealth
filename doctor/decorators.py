from django.contrib import messages
from django.shortcuts import redirect


def authorization_required(view_func):
    def wrapper_func(request,  *args, **kwargs):
        if request.user.doctor.is_verified:
            request.doctor = request.user.doctor
            return view_func(request, *args, **kwargs)
        else:
            messages.info(request, "Your doctor account has not been authorized or verified. "
                                   "Kindly contact support for a follow up")
            return redirect(request.META['HTTP_REFERER'])
    return wrapper_func
