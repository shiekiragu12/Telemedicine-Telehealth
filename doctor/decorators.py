from django.contrib import messages
from django.shortcuts import redirect


def doctor_and_authorization_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.doctor:
            if request.user.doctor.is_verified:
                request.doctor = request.user.doctor
                return view_func(request, *args, **kwargs)
            else:
                messages.info(request, "Your doctor account has not been authorized or verified. "
                                       "Kindly contact support for a follow up")
                return redirect('index')
        else:
            messages.warning(request, "Only doctors are allowed at this page")
            return redirect('index')

    return wrapper_func
