from .base_agent import BaseAgent
from tools.github_tool import GitHubTool


class GitHubAgent(BaseAgent):

    name = "GitHub Agent"

    description = "Handles GitHub repository and cloud development questions"

    def __init__(self):
        self.github_tool = GitHubTool()

    def can_handle(self, request):

        github_keywords = [
            "github",
            "git",
            "repository",
            "repositories",
            "repo",
            "repos",
            "pull request",
            "pull requests",
            "pr",
            "issue",
            "issues",
            "git status",
            "repository status",
            "cloud",
            "cloud deployment",
            "deployment",
        ]

        request_lower = request.lower()

        return any(keyword in request_lower for keyword in github_keywords)

    def get_required_permission(self, request):

        return "view_github"

    def process(self, request, user, credentials=None):

        request_lower = request.lower()

        # -----------------------------------------
        # Repository Status
        # -----------------------------------------

        if (
            "status" in request_lower
            or "repository" in request_lower
            or "repositories" in request_lower
            or "repo" in request_lower
            or "github" in request_lower
        ):

            result = self.github_tool.execute(
                "get_repository_status",
                user,
            )

            if result.get("status") == "success":

                data = result.get("data", {})

                message = (
                    "GitHub Repository Status:\n"
                    f"Repositories: {data.get('repositories', 0)}\n"
                    f"Open Issues: {data.get('open_issues', 0)}\n"
                    f"Open Pull Requests: "
                    f"{data.get('open_pull_requests', 0)}"
                )

                return {
                    "agent": self.name,
                    "status": "success",
                    "data": data,
                    "message": message,
                }

        # -----------------------------------------
        # Cloud / Deployment Information
        # -----------------------------------------

        if (
            "cloud" in request_lower
            or "deployment" in request_lower
            or "deploy" in request_lower
        ):

            return {
                "agent": self.name,
                "status": "success",
                "data": {
                    "message": (
                        "Cloud deployment information is "
                        "currently available as an MVP feature."
                    )
                },
                "message": (
                    "Cloud deployment information is "
                    "currently available as an MVP feature."
                ),
            }

        # -----------------------------------------
        # Unsupported Request
        # -----------------------------------------

        return {
            "agent": self.name,
            "status": "error",
            "data": {},
            "message": (
                "The requested GitHub or Cloud "
                "information is not currently supported."
            ),
        }
