from django.urls import URLPattern, path

from accounts.views import SignUpView

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
]