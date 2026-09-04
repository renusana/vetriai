from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils import timezone

from google.oauth2.credentials import Credentials

from .google_calendar import create_google_flow, get_calendar_service
from .serializers import (
    UserRoleSerializer,
    ConversationSerializer,
)
from .models import UserProfile, Conversation, ChatMessage

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from permissions.permission_engine import PermissionEngine
from agents.orchestrator import AIOrchestrator


@api_view(["GET"])
def hello_api(request):
    return Response(
        {
            "success": True,
            "message": "Hello from Django API!",
            "project": "Vetri AI Multi Agent",
        }
    )


def get_user_role(user):
    # Superuser is always treated as admin
    if user.is_superuser:
        return "admin"

    # Get application role
    profile, created = UserProfile.objects.get_or_create(
        user=user,
        defaults={"role": "employee"},
    )

    return profile.role


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def chat_api(request):

    # -------------------------------------------------
    # Get message from React/frontend
    # -------------------------------------------------

    message = request.data.get("message")

    # Get conversation ID from React/frontend
    conversation_id = request.data.get("conversation_id")

    # Validate message
    if not message:
        return Response(
            {
                "status": "error",
                "message": "Message is required.",
            },
            status=400,
        )

    # -------------------------------------------------
    # Current User
    # -------------------------------------------------

    user = request.user

    role = get_user_role(user)

    print("USER REQUEST:", message)
    print("CURRENT USER:", user.username)
    print("CURRENT ROLE:", role)

    # -------------------------------------------------
    # Conversation History
    # -------------------------------------------------

    if conversation_id:

        try:
            conversation = Conversation.objects.get(
                id=conversation_id,
                user=user,
            )

        except Conversation.DoesNotExist:
            return Response(
                {
                    "status": "error",
                    "message": "Conversation not found.",
                },
                status=404,
            )

    else:

        conversation = Conversation.objects.create(
            user=user,
            title="New Conversation",
        )

    # -------------------------------------------------
    # Save User Message
    # -------------------------------------------------

    ChatMessage.objects.create(
        conversation=conversation,
        sender="user",
        content=message,
    )

    # -------------------------------------------------
    # AI Orchestrator + Google Calendar Debug
    # -------------------------------------------------

    try:

        print("STEP 1: Creating AIOrchestrator")

        orchestrator = AIOrchestrator()

        print("STEP 2: Getting Google Calendar credentials")

        google_credentials = request.session.get("google_calendar_credentials")

        # Do NOT print the actual credentials.
        # Only print whether credentials exist.
        print(
            "GOOGLE CALENDAR CREDENTIALS PRESENT:",
            bool(google_credentials),
        )

        print("STEP 3: Calling orchestrator.process_request")

        result = orchestrator.process_request(
            request=message,
            user=user,
            role=role,
            credentials=google_credentials,
        )

        print("STEP 4: Orchestrator completed successfully")

    except Exception as error:

        import traceback

        print("========== CHAT API ERROR ==========")
        print("ERROR:", str(error))
        traceback.print_exc()
        print("====================================")

        return Response(
            {
                "status": "error",
                "message": "Chat processing failed.",
            },
            status=500,
        )

    # -------------------------------------------------
    # Confidence & Source Information
    # -------------------------------------------------

    result["metadata"] = {
        "source": result.get(
            "agent",
            "Vetri AI",
        ),
        "updated_at": timezone.now().isoformat(),
        "confidence": ("High" if result.get("status") == "success" else "Low"),
    }

    # -------------------------------------------------
    # Save AI Response
    # -------------------------------------------------

    assistant_response = result.get(
        "response",
        "",
    )

    ChatMessage.objects.create(
        conversation=conversation,
        sender="assistant",
        content=assistant_response,
    )

    # Return conversation information
    result["conversation_id"] = conversation.id

    return Response(result)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def conversations_api(request):
    """
    List the current user's conversations
    or create a new conversation.
    """

    user = request.user

    if request.method == "GET":

        conversations = Conversation.objects.filter(user=user)

        serializer = ConversationSerializer(
            conversations,
            many=True,
        )

        return Response(
            {
                "status": "success",
                "conversations": serializer.data,
            }
        )

    # POST - create new conversation

    title = request.data.get(
        "title",
        "New Conversation",
    )

    conversation = Conversation.objects.create(
        user=user,
        title=title,
    )

    serializer = ConversationSerializer(conversation)

    return Response(
        {
            "status": "success",
            "conversation": serializer.data,
        },
        status=201,
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def conversation_detail_api(request, conversation_id):
    """
    Return one conversation belonging to the
    currently authenticated user.
    """

    user = request.user

    try:

        conversation = Conversation.objects.get(
            id=conversation_id,
            user=user,
        )

    except Conversation.DoesNotExist:

        return Response(
            {
                "status": "error",
                "message": "Conversation not found.",
            },
            status=404,
        )

    serializer = ConversationSerializer(conversation)

    return Response(
        {
            "status": "success",
            "conversation": serializer.data,
        }
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def current_user_api(request):

    user = request.user

    role = get_user_role(user)

    name = user.get_full_name().strip()

    if not name:
        name = user.username

    role_names = {
        "admin": "Administrator",
        "manager": "Manager",
        "hr": "HR",
        "sales": "Sales",
        "employee": "Employee",
    }

    return Response(
        {
            "username": user.username,
            "name": name,
            "email": user.email,
            "role": role_names.get(
                role,
                "Employee",
            ),
            "role_code": role,
        }
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_roles_api(request):

    profiles = UserProfile.objects.select_related("user").all()

    serializer = UserRoleSerializer(
        profiles,
        many=True,
    )

    return Response(
        {
            "status": "success",
            "users": serializer.data,
        }
    )


def google_calendar_login(request):
    """
    Start Google Calendar OAuth login.
    """

    flow = create_google_flow()

    authorization_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent",
    )

    # Save OAuth state and PKCE code verifier
    request.session["google_oauth_state"] = state
    request.session["google_oauth_code_verifier"] = flow.code_verifier

    return redirect(authorization_url)


def google_calendar_test(request):
    """
    Test Google Calendar API access using stored OAuth credentials.
    """

    stored_credentials = request.session.get("google_calendar_credentials")

    if not stored_credentials:

        return JsonResponse(
            {
                "status": "error",
                "message": ("Google Calendar is not connected. " "Please login first."),
            },
            status=401,
        )

    credentials = Credentials(
        token=stored_credentials["token"],
        refresh_token=stored_credentials.get("refresh_token"),
        token_uri=stored_credentials["token_uri"],
        client_id=stored_credentials["client_id"],
        client_secret=stored_credentials["client_secret"],
        scopes=stored_credentials["scopes"],
    )

    service = get_calendar_service(credentials)

    calendar_list = service.calendarList().list().execute()

    calendars = []

    for calendar in calendar_list.get(
        "items",
        [],
    ):

        calendars.append(
            {
                "id": calendar.get("id"),
                "summary": calendar.get("summary"),
                "description": calendar.get("description"),
                "primary": calendar.get(
                    "primary",
                    False,
                ),
            }
        )

    return JsonResponse(
        {
            "status": "success",
            "message": ("Google Calendar API is working."),
            "calendars": calendars,
        }
    )


def google_calendar_callback(request):
    """
    Handle Google's OAuth callback.
    """

    state = request.session.get("google_oauth_state")

    code_verifier = request.session.get("google_oauth_code_verifier")

    if not state:

        return JsonResponse(
            {
                "status": "error",
                "message": ("OAuth session state is missing."),
            },
            status=400,
        )

    if not code_verifier:

        return JsonResponse(
            {
                "status": "error",
                "message": ("OAuth code verifier is missing."),
            },
            status=400,
        )

    flow = create_google_flow()

    # Restore OAuth state and PKCE verifier
    flow.state = state
    flow.code_verifier = code_verifier

    flow.fetch_token(authorization_response=request.build_absolute_uri())

    credentials = flow.credentials

    request.session["google_calendar_credentials"] = {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes,
    }

    # OAuth flow is complete
    request.session.pop(
        "google_oauth_state",
        None,
    )

    request.session.pop(
        "google_oauth_code_verifier",
        None,
    )

    return JsonResponse(
        {
            "status": "success",
            "message": ("Google Calendar connected successfully."),
        }
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def permissions_api(request):
    """
    Return all role-based permissions.
    """

    permission_engine = PermissionEngine()

    roles = {}

    for role, permissions in permission_engine.ROLE_PERMISSIONS.items():

        roles[role] = sorted(list(permissions))

    return Response(
        {
            "status": "success",
            "roles": roles,
        }
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def agents_api(request):
    """
    Return all available AI agents.
    """

    return Response(
        {
            "status": "success",
            "agents": [
                {
                    "name": "Calendar Agent",
                    "description": (
                        "Handles Google Calendar events "
                        "and calendar-related questions"
                    ),
                },
                {
                    "name": "HR Agent",
                    "description": ("Handles employee and " "HR-related questions"),
                },
                {
                    "name": "Sales Agent",
                    "description": ("Handles sales and CRM-related " "questions"),
                },
                {
                    "name": "Project Agent",
                    "description": ("Handles project and task-related " "questions"),
                },
                {
                    "name": "Finance Agent",
                    "description": (
                        "Handles finance and financial " "summary questions"
                    ),
                },
                {
                    "name": "Marketing Agent",
                    "description": ("Handles marketing-related " "questions"),
                },
                {
                    "name": "Developer Agent",
                    "description": ("Handles software development " "questions"),
                },
                {
                    "name": "QA Agent",
                    "description": (
                        "Handles quality assurance " "and testing questions"
                    ),
                },
                {
                    "name": "Operations Agent",
                    "description": (
                        "Handles business operations " "and workflow questions"
                    ),
                },
                {
                    "name": "Reporting Agent",
                    "description": ("Handles business reports " "and summaries"),
                },
                {
                    "name": "GitHub Agent",
                    "description": (
                        "Handles GitHub repository " "and cloud development questions"
                    ),
                },
            ],
        }
    )
