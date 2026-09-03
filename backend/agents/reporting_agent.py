from .base_agent import BaseAgent
from knowledge_base.rag import RAGSystem


class ReportingAgent(BaseAgent):

    name = "Reporting Agent"

    description = "Handles business reports and summaries"

    def __init__(self):
        self.rag = RAGSystem()

    def can_handle(self, request):

        reporting_keywords = [
            "report",
            "reports",
            "reporting",
            "summary",
            "summarize",
            "business report",
            "daily report",
            "bo report",
        ]

        request_lower = request.lower()

        return any(keyword in request_lower for keyword in reporting_keywords)

    def get_required_permission(self, request):

        request_lower = request.lower()

        # ==========================================
        # Knowledge Base / Reporting SOP questions
        # ==========================================

        knowledge_keywords = [
            "policy",
            "sop",
            "process",
            "procedure",
            "how can",
            "how do",
            "how should",
            "reporting process",
            "reporting sop",
            "business reporting",
        ]

        is_knowledge_question = any(
            keyword in request_lower for keyword in knowledge_keywords
        )

        if is_knowledge_question:
            return None

        # ==========================================
        # Normal report access requires permission
        # ==========================================

        return "view_reports"

    def process(
        self,
        request,
        user,
        credentials=None,
    ):

        request_lower = request.lower()

        # ==========================================
        # Knowledge Base / Reporting SOP Questions
        # ==========================================

        knowledge_keywords = [
            "policy",
            "sop",
            "process",
            "procedure",
            "how can",
            "how do",
            "how should",
            "reporting process",
            "reporting sop",
            "business reporting",
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

        # ==========================================
        # Existing Business Report
        # ==========================================

        return {
            "agent": self.name,
            "status": "success",
            "data": {
                "new_leads": 12,
                "pending_followups": 5,
                "pending_orders": 3,
                "delayed_projects": 2,
                "employees_on_leave": 2,
            },
            "message": (
                "Today's BO report: "
                "12 new leads, 5 pending sales follow-ups, "
                "3 pending orders, 2 delayed projects, "
                "and 2 employees on leave."
            ),
        }
