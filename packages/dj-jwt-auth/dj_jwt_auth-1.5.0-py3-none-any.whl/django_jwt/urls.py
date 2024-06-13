from django.urls import path

from django_jwt import views

urlpatterns = [
    path("oidc/callback/", views.ReceiveRedirectView.as_view(), name="receive_redirect_view"),
    path("oidc/logout/", views.silent_sso_check, name="silent_sso_check"),
    path("oidc/", views.StartOIDCAuthView.as_view(), name="start_oidc_auth"),
]
