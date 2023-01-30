from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q

from .decorators import unauthenticated_user
from django.contrib import messages
from facilities.models import County, FacilitySpeciality, Facility


@unauthenticated_user
def account_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        next_url = request.GET.get('next', None)

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have successfully logged In!')
            return redirect('index')
        else:
            messages.error(request, 'Login failed! Check your username and password.')
            return render(request, template_name='auth/signin.html', context={})

    return render(request, template_name='auth/signin.html', context={})


@unauthenticated_user
def account_signup(request):
    if request.method == 'POST':

        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        password1 = request.POST.get('password1')

        existinguser = User.objects.filter(Q(username=username) | Q(email=email)).first()
        user = User(first_name=fname, last_name=lname, email=email, username=username)

        if password != password1:
            messages.error(request, 'Passwords do not match')
            return render(request, template_name='auth/sign-up.html', context={"user": user})

        elif existinguser is not None:
            messages.error(request, 'User with similar credentials already exists. Check your username')
            return render(request, template_name='auth/sign-up.html', context={"user": user})

        else:
            user.save()
            user.set_password(password)
            user.save()
            messages.success(request, 'Account created successfully')
            return redirect('signin')

    return render(request, template_name='auth/sign-up.html', context={})


def account_logout(request):
    messages.success(request, 'You have successfully logged out!')
    logout(request)
    return redirect('index')


@login_required(login_url='signin')
def account_change_profile_pic(request):
    if request.method == 'POST':
        userp = request.user.profile
        pic = request.FILES.get('profile_photo')
        userp.profile_photo = pic
        userp.save()
        messages.success(request, 'You have successfully changed your profile picture')
        return redirect('account_profile')


@login_required(login_url='signin')
def account_change_password(request):
    if request.method == 'POST':
        user = request.user
        old_pass = request.POST.get('old_password')
        new_pass = request.POST.get('password')
        new_pass_repeat = request.POST.get('password1')
        if user.check_password(old_pass):
            if new_pass == new_pass_repeat:
                try:
                    pass_validate = validate_password(new_pass, user=None, password_validators=None)
                    if pass_validate is None:
                        user.set_password(new_pass)
                        user.save()
                        messages.success(request, 'Password change was successful')
                        return redirect('account_profile')
                except ValidationError:
                    messages.error(request,
                                   'The new password you entered does not meet the minimum requirements(8 characters '
                                   'minimum, should contain numbers, and characters)')
                    return redirect('account_profile')
            else:
                messages.error(request, 'Passwords do not match')
                return redirect('account_profile')
        else:
            messages.error(request, 'The old password you gave is incorrect')
            return redirect('account_profile')


@login_required(login_url='signin')
def account_profile(request):

    context = {
        'my_facilities': Facility.objects.filter(owner=request.user),
        'counties': County.objects.all(),
        'specialities': FacilitySpeciality.objects.all(),
    }
    return render(request, template_name='account/profile.html', context=context)


@login_required(login_url='signin')
def account_edit(request):
    if request.method == 'POST':
        fname = request.POST.get('first_name')
        lname = request.POST.get('last_name')
        email = request.POST.get('email')
        # username = request.POST.get('username')

        user = request.user
        user.first_name = fname
        user.last_name = lname
        user.email = email
        # user.username = username
        user.save()

        messages.success(request, 'Account information updated successfully')

        return redirect('account_profile')

    return redirect('account_profile')


@login_required(login_url='signin')
def account_profile_edit(request):
    if request.method == 'POST':
        pnumber = request.POST.get('phone_number')
        address = request.POST.get('address')
        country = request.POST.get('country')
        gender = request.POST.get('gender')
        city = request.POST.get('city')
        postal_code = request.POST.get('postal_code')

        user = request.user
        user.profile.phone_number = pnumber
        user.profile.address = address
        user.profile.country = country
        user.profile.gender = gender
        user.profile.city = city
        user.profile.postal_code = postal_code

        user.profile.save()

        messages.success(request, 'Account Profile information updated successfully')

        return redirect('account_profile')

    return redirect('account_profile')
