from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.shortcuts import render, redirect

from facilities.models import County, Speciality, Facility, QualificationCourse
from .decorators import unauthenticated_user
from .models import Profile
from .forms import ProfileForm
from website.models import Notification


@unauthenticated_user
def account_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        next_url = request.POST.get('next', None)

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have successfully logged In!')
            return redirect(next_url) if next_url else redirect('index')
        else:
            messages.error(request, 'Login failed! Check your username and password.')
            return render(request, template_name='auth/signin.html', context={})

    return render(request, template_name='auth/signin.html', context={})


@unauthenticated_user
def register_as(request):
    context = {
        'courses': QualificationCourse.objects.all(),
    }

    return render(request, template_name='auth/register/register.html', context=context)


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
        if getattr(request.user, 'profile', None):
            userp = request.user.profile
            pic = request.FILES.get('profile_photo')
            userp.profile_photo = pic
            userp.save()
        else:
            profile = Profile.objects.create(user=request.user)
            pic = request.FILES.get('profile_photo')
            profile.profile_photo = pic
            profile.save()
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
        'specialities': Speciality.objects.all(),
    }
    return render(request, template_name='account/profile.html', context=context)


@login_required(login_url='signin')
def account_notifications(request):

    context = {
    }
    return render(request, template_name='account/notifications.html', context=context)


@login_required(login_url='signin')
def notification_read(request, pk):
    notification = Notification.objects.filter(id=pk).first()
    if notification:
        if notification.to_admin:
            if request.user.is_superuser:
                messages.success(request, 'Marked as read')
                notification.read = True
            else:
                messages.warning(request, 'You will be blocked, no impersonation')
        else:
            if notification.to_user == request.user:
                messages.success(request, 'Marked as read')
                notification.read = True
            else:
                messages.warning(request, 'Only owners of notifications can mark them as read')
        notification.save()
    else:
        messages.error(request, 'No such notification', extra_tags='danger')
    context = {
    }
    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='signin')
def notification_delete(request, pk):
    notification = Notification.objects.filter(id=pk).first()
    if notification:
        if notification.to_admin:
            if request.user.is_superuser:
                messages.success(request, 'Deleted')
                notification.delete()
            else:
                messages.warning(request, 'You will be blocked, no impersonation')
        else:
            if notification.to_user == request.user:
                messages.success(request, 'Marked as read')
                notification.delete()
            else:
                messages.warning(request, 'Only owners of notifications can mark them as read')
    else:
        messages.error(request, 'No such notification', extra_tags='danger')
    context = {
    }
    return redirect(request.META.get('HTTP_REFERER'))


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
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account Profile information updated successfully')
        else:
            messages.error(request, 'Could not update your account information. Try again', extra_tags='danger')

        return redirect('account_profile')

    return redirect('account_profile')

