from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path('register/', account_signup, name="signup"),
    path('login/', account_login, name="signin"),
    path('logout/', account_logout, name="logout"),

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
