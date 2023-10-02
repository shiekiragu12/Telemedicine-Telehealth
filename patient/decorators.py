from django.contrib import messages
from django.shortcuts import redirect


def patient_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.patient:
            return view_func(request, *args, **kwargs)
        else:
            messages.warning(request, "Only patients are allowed at this page")
            return redirect('index')

    return wrapper_func
