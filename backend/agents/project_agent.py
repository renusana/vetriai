from .base_agent import BaseAgent
from tools.project_tool import ProjectTool
from knowledge_base.rag import RAGSystem


class ProjectAgent(BaseAgent):

    name = "Project Agent"

    description = "Handles project status and project tracking questions"

    def __init__(self):
        self.project_tool = ProjectTool()
        self.rag = RAGSystem()

    def can_handle(self, request):

        project_keywords = [
            "project",
            "projects",
            "delayed",
            "delay",
            "deadline",
            "deadlines",
            "task",
            "tasks",
            "milestone",
            "milestones",
            "project status",
            "project policy",
            "project sop",
            "project process",
        ]

        request_lower = request.lower()

        return any(keyword in request_lower for keyword in project_keywords)

    def get_required_permission(self, request):

        request_lower = request.lower()

        # -----------------------------------------
        # Knowledge Base / Project SOP questions
        # -----------------------------------------

        knowledge_keywords = [
            "policy",
            "sop",
            "process",
            "procedure",
            "how can",
            "how do",
            "how should",
            "project management",
            "project process",
        ]

        is_knowledge_question = any(
            keyword in request_lower for keyword in knowledge_keywords
        )

        if is_knowledge_question:
            return None

        # -----------------------------------------
        # Project deadlines
        # -----------------------------------------

        if "deadline" in request_lower or "deadlines" in request_lower:
            return "view_project_status"

        # -----------------------------------------
        # Project status / delayed projects
        # -----------------------------------------

        if (
            "status" in request_lower
            or "delayed" in request_lower
            or "delay" in request_lower
        ):
            return "view_project_status"

        # -----------------------------------------
        # Employee's own tasks
        # -----------------------------------------

        if "task" in request_lower or "tasks" in request_lower:

            if "my" in request_lower or "own" in request_lower:
                return "view_own_tasks"

            return "view_projects"

        # -----------------------------------------
        # Employee's own projects
        # -----------------------------------------

        if "project" in request_lower or "projects" in request_lower:

            if "my" in request_lower or "own" in request_lower:
                return "view_own_projects"

            return "view_projects"

        return "view_projects"

    def process(self, request, user, credentials=None):

        request_lower = request.lower()

        # =========================================
        # Knowledge Base / Project SOP Questions
        # =========================================

        knowledge_keywords = [
            "policy",
            "sop",
            "process",
            "procedure",
            "how can",
            "how do",
            "how should",
            "project management",
            "project process",
        ]

        is_knowledge_question = any(
            keyword in request_lower for keyword in knowledge_keywords
        )

        if is_knowledge_question:

            knowledge_answer = self.rag.generate_answer(request)

            if knowledge_answer:

                return {
                    "agent": self.name,
                    "status": "success",
                    "data": {
                        "knowledge_answer": knowledge_answer,
                    },
                    "message": knowledge_answer,
                }

        # -----------------------------------------
        # Delayed Projects
        # -----------------------------------------

        if "delayed" in request_lower or "delay" in request_lower:

            result = self.project_tool.execute(
                "get_delayed_projects",
                user,
            )

            if result.get("status") == "success":

                data = result.get("data", {})

                projects = data.get(
                    "delayed_projects",
                    [],
                )

                if not projects:

                    message = "There are no delayed projects."

                else:

                    lines = []

                    for project in projects:

                        lines.append(
                            f"{project['name']} " f"({project['delay_days']} days)"
                        )

                    message = (
                        f"There are {len(projects)} "
                        "delayed projects:\n" + "\n".join(lines)
                    )

                return {
                    "agent": self.name,
                    "status": "success",
                    "data": data,
                    "message": message,
                }

        # -----------------------------------------
        # Project Status
        # -----------------------------------------

        if "status" in request_lower:

            result = self.project_tool.execute(
                "get_project_status",
                user,
            )

            if result.get("status") == "success":

                data = result.get("data", {})

                message = (
                    "Project Status:\n"
                    f"Active: {data.get('active_projects', 0)}\n"
                    f"Completed: {data.get('completed_projects', 0)}\n"
                    f"Delayed: {data.get('delayed_projects', 0)}"
                )

                return {
                    "agent": self.name,
                    "status": "success",
                    "data": data,
                    "message": message,
                }

        # -----------------------------------------
        # Project Deadlines
        # -----------------------------------------

        if "deadline" in request_lower or "deadlines" in request_lower:

            result = self.project_tool.execute(
                "get_project_deadlines",
                user,
            )

            if result.get("status") == "success":

                data = result.get("data", {})

                deadlines = data.get(
                    "deadlines",
                    [],
                )

                if not deadlines:

                    message = "There are no upcoming deadlines."

                else:

                    lines = []

                    for deadline in deadlines:

                        lines.append(
                            f"{deadline['project']} - " f"{deadline['deadline']}"
                        )

                    message = "Upcoming Project Deadlines:\n" + "\n".join(lines)

                return {
                    "agent": self.name,
                    "status": "success",
                    "data": data,
                    "message": message,
                }

        # -----------------------------------------
        # Project Tasks
        # -----------------------------------------

        if "task" in request_lower:

            result = self.project_tool.execute(
                "get_project_tasks",
                user,
            )

            if result.get("status") == "success":

                data = result.get("data", {})

                tasks = data.get(
                    "tasks",
                    [],
                )

                if not tasks:

                    message = "There are no project tasks."

                else:

                    lines = []

                    for task in tasks:

                        lines.append(
                            f"{task['project']}: "
                            f"{task['task']} "
                            f"({task['status']})"
                        )

                    message = "Current Project Tasks:\n" + "\n".join(lines)

                return {
                    "agent": self.name,
                    "status": "success",
                    "data": data,
                    "message": message,
                }

        # -----------------------------------------
        # Projects
        # -----------------------------------------

        if "project" in request_lower:

            result = self.project_tool.execute(
                "get_projects",
                user,
            )

            if result.get("status") == "success":

                data = result.get("data", {})

                projects = data.get(
                    "projects",
                    [],
                )

                if not projects:

                    message = "There are no projects."

                else:

                    names = [project["name"] for project in projects]

                    message = (
                        f"There are {len(projects)} "
                        "projects: " + ", ".join(names) + "."
                    )

                return {
                    "agent": self.name,
                    "status": "success",
                    "data": data,
                    "message": message,
                }

        # -----------------------------------------
        # Unsupported Request
        # -----------------------------------------

        return {
            "agent": self.name,
            "status": "error",
            "data": {},
            "message": (
                "The requested project information " "is not currently supported."
            ),
        }
