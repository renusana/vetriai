from .base_agent import BaseAgent


class DeveloperAgent(BaseAgent):

    name = "Developer Agent"

    description = (
        "Handles software development, code, technical, and programming questions"
    )

    def can_handle(self, request):

        developer_keywords = [
            "developer",
            "development",
            "code",
            "coding",
            "programming",
            "python",
            "django",
            "react",
            "javascript",
            "bug",
            "debug",
            "debugging",
            "error",
            "technical",
            "software",
            "api",
            "database",
        ]

        request_lower = request.lower()

        return any(keyword in request_lower for keyword in developer_keywords)

    def get_required_permission(self, request):

        return "view_developer"

    def process(self, request, user, credentials=None):

        request_lower = request.lower()

        if any(
            keyword in request_lower
            for keyword in [
                "developer",
                "development",
                "code",
                "coding",
                "programming",
                "python",
                "django",
                "react",
                "javascript",
                "bug",
                "debug",
                "debugging",
                "error",
                "technical",
                "software",
                "api",
                "database",
            ]
        ):

            data = {
                "active_projects": 4,
                "open_bugs": 8,
                "completed_tasks": 27,
                "deployments": 6,
            }

            message = (
                "Developer Summary:\n"
                f"Active Projects: {data['active_projects']}\n"
                f"Open Bugs: {data['open_bugs']}\n"
                f"Completed Tasks: {data['completed_tasks']}\n"
                f"Deployments: {data['deployments']}"
            )

            return {
                "agent": self.name,
                "status": "success",
                "data": data,
                "message": message,
            }

        return {
            "agent": self.name,
            "status": "error",
            "data": {},
            "message": "The requested developer information is not currently supported.",
        }
