import django.urls
import identity.views

urlpatterns = [
    django.urls.path(
        "session/", identity.views.SessionListView.as_view(), name="auth-session-list"
    ),
    django.urls.path(
        "user/", identity.views.UserListView.as_view(), name="auth-user-list"
    ),
]
