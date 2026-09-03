from django.urls import path

from .views import (
    hello_api,
    chat_api,
    current_user_api,
    user_roles_api,
    permissions_api,
    agents_api,
    conversations_api,
    conversation_detail_api,
    google_calendar_login,
    google_calendar_callback,
    google_calendar_test,
)

urlpatterns = [
    path(
        "hello/",
        hello_api,
        name="hello-api",
    ),
    path(
        "chat/",
        chat_api,
        name="chat-api",
    ),
    path(
        "auth/me/",
        current_user_api,
        name="current-user-api",
    ),
    path(
        "user-roles/",
        user_roles_api,
        name="user_roles_api",
    ),
    path(
        "permissions/",
        permissions_api,
        name="permissions_api",
    ),
    path(
        "agents/",
        agents_api,
        name="agents_api",
    ),
    # Conversation History
    path(
        "conversations/",
        conversations_api,
        name="conversations-api",
    ),
    path(
        "conversations/<int:conversation_id>/",
        conversation_detail_api,
        name="conversation-detail-api",
    ),
    # Google Calendar
    path(
        "calendar/login/",
        google_calendar_login,
        name="google-calendar-login",
    ),
    path(
        "calendar/oauth2callback/",
        google_calendar_callback,
        name="google-calendar-callback",
    ),
    path(
        "calendar/test/",
        google_calendar_test,
        name="google-calendar-test",
    ),
]
