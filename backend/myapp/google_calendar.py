import os

from django.conf import settings

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


def get_credentials_file():
    return os.path.join(
        settings.BASE_DIR,
        "google_credentials.json",
    )


def create_google_flow():
    flow = Flow.from_client_secrets_file(
        get_credentials_file(),
        scopes=SCOPES,
        redirect_uri="http://127.0.0.1:8000/api/calendar/oauth2callback/",
    )

    return flow


def get_calendar_service(credentials):
    return build(
        "calendar",
        "v3",
        credentials=credentials,
    )
