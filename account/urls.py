from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path('register/', account_signup, name="signup"),
    path('login/', account_login, name="signin"),
    path('logout/', account_logout, name="logout"),

    path('profile/', account_profile, name="account_profile"),
    path('edit/', account_edit, name="account_edit"),
    path('change-password/', account_change_password, name="account_change_password"),
    path('profile/edit/', account_profile_edit, name="account_profile_edit"),
    path('profile/photo/edit/', account_change_profile_pic, name="account_profile_photo_edit"),

    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='user/account/password_reset.html'),
         name="password_reset"),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='user/account'
                                                                                        '/password_reset_done.html'),
         name="password_reset_done"),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='user/account/password_reset_confirm.html'),
         name="password_reset_confirm"),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='user/account/password_reset_complete.html'),
         name="password_reset_complete"),
]
