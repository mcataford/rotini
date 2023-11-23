import django.urls
import auth.views

urlpatterns = [
    django.urls.path(
        "session/", auth.views.SessionListView.as_view(), name="auth-session-list"
    ),
    django.urls.path("user/", auth.views.UserListView.as_view(), name="auth-user-list"),
]
