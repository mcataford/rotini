import django.urls
import auth.views

urlpatterns = [
    django.urls.path("auth/login/", auth.views.LoginView.as_view(), name="auth-login"),
    django.urls.path("user/", auth.views.UserListView.as_view(), name="auth-user-list"),
]
