"""conceptalbums URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import include, path, re_path

from django.views.defaults import page_not_found
from django.contrib.auth import views as auth_views
from allauth.account.views import confirm_email

from . import views

urlpatterns = [
    # disabling API password reset views
    re_path(
        "^api/authentication/password/reset/",
        page_not_found,
        {"exception": Exception()},
    ),
    # routes
    path(
        "authentication/password/reset/",
        auth_views.PasswordResetView.as_view(),
        name="reset_password",
    ),
    path(
        "authentication/password/reset/done/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "authentication/password/reset/confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "authentication/password/reset/complete/",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    path("api/authentication/", include("dj_rest_auth.urls")),
    path("api/authentication/registration/", include("dj_rest_auth.registration.urls")),
    # must be after dj_rest_auth.registration.urls
    re_path(
        r"^authentication/registration/account-confirm-email/(?P<key>.+)/$",
        confirm_email,
        name="account_confirm_email",
    ),
    path("email_success/", views.email_success, name="email_success"),
]
