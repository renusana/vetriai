from .base_agent import BaseAgent


class OperationsAgent(BaseAgent):

    name = "Operations Agent"

    description = "Handles operations, processes, workflows, and operational performance questions"

    def can_handle(self, request):

        operations_keywords = [
            "operations",
            "operation",
            "operational",
            "workflow",
            "workflows",
            "process",
            "processes",
            "operational performance",
            "operations summary",
            "productivity",
            "efficiency",
        ]

        request_lower = request.lower()

        return any(keyword in request_lower for keyword in operations_keywords)

    def get_required_permission(self, request):
        return "view_operations"

    def process(self, request, user, credentials=None):

        request_lower = request.lower()

        if any(
            keyword in request_lower
            for keyword in [
                "operations",
                "operation",
                "operational",
                "workflow",
                "workflows",
                "process",
                "processes",
                "productivity",
                "efficiency",
            ]
        ):

            data = {
                "active_workflows": 8,
                "completed_processes": 42,
                "pending_tasks": 15,
                "efficiency": "88%",
            }

            message = (
                "Operations Summary:\n"
                f"Active Workflows: {data['active_workflows']}\n"
                f"Completed Processes: {data['completed_processes']}\n"
                f"Pending Tasks: {data['pending_tasks']}\n"
                f"Efficiency: {data['efficiency']}"
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
            "message": "The requested operations information is not currently supported.",
        }
