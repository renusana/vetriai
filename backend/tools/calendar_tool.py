from google.oauth2.credentials import Credentials

from myapp.google_calendar import get_calendar_service


class CalendarTool:
    """
    Tool for reading Google Calendar events.
    """

    name = "calendar_tool"
    description = "Handles Google Calendar operations."

    def execute(self, action, user=None, credentials=None):

        if not credentials:
            return {
                "status": "error",
                "message": "Google Calendar is not connected.",
            }

        if action not in ["get_today_events", "get_tomorrow_events"]:
            return {
                "status": "error",
                "message": "Calendar action not supported.",
            }

        try:
            google_credentials = Credentials(
                token=credentials["token"],
                refresh_token=credentials.get("refresh_token"),
                token_uri=credentials["token_uri"],
                client_id=credentials["client_id"],
                client_secret=credentials["client_secret"],
                scopes=credentials["scopes"],
            )

            service = get_calendar_service(google_credentials)

            from datetime import datetime, timedelta, timezone

            now = datetime.now(timezone.utc)

            start_of_today = now.replace(
                hour=0,
                minute=0,
                second=0,
                microsecond=0,
            )

            if action == "get_today_events":
                start_time = start_of_today
                end_time = start_of_today + timedelta(days=1)

            else:
                start_time = start_of_today + timedelta(days=1)
                end_time = start_of_today + timedelta(days=2)

            events_result = (
                service.events()
                .list(
                    calendarId="primary",
                    timeMin=start_time.isoformat(),
                    timeMax=end_time.isoformat(),
                    singleEvents=True,
                    orderBy="startTime",
                )
                .execute()
            )

            events = []

            for event in events_result.get("items", []):

                start = event.get("start", {})

                event_time = start.get(
                    "dateTime",
                    start.get("date"),
                )

                events.append(
                    {
                        "id": event.get("id"),
                        "title": event.get(
                            "summary",
                            "Untitled event",
                        ),
                        "time": event_time,
                        "description": event.get("description"),
                    }
                )

            return {
                "status": "success",
                "events": events,
                "total": len(events),
            }

        except Exception as exc:

            return {
                "status": "error",
                "message": f"Calendar API error: {str(exc)}",
            }
