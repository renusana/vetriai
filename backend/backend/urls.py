from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from myapp.views import google_calendar_test
from myapp.views import (
    google_calendar_login,
    google_calendar_test,
    google_calendar_callback,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("myapp.urls")),
    path("api/auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/audit-logs/", include("audit_logs.urls")),
    path("api/notifications/", include("notifications.urls")),
    path("api/approvals/", include("approvals.urls")),
    path(
        "api/calendar/login/",
        google_calendar_login,
        name="google-calendar-login",
    ),
    path(
        "api/calendar/oauth2callback/",
        google_calendar_callback,
        name="google-calendar-callback",
    ),
    path(
        "api/calendar/test/",
        google_calendar_test,
        name="google-calendar-test",
    ),
]
