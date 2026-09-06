from .base_agent import BaseAgent
from knowledge_base.rag import RAGSystem
from tools.reporting_tool import ReportingTool


class ReportingAgent(BaseAgent):

    name = "Reporting Agent"

    description = "Handles business reports and summaries"

    def __init__(self):
        self.rag = RAGSystem()
        self.reporting_tool = ReportingTool()

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
        # Generate Business Report using ReportingTool
        # ==========================================

        report_result = self.reporting_tool.execute(
            "generate_daily_report",
            user=user,
        )

        if report_result.get("status") != "success":

            return {
                "agent": self.name,
                "status": "error",
                "data": {},
                "message": report_result.get(
                    "message", "Unable to generate the daily report."
                ),
            }

        report = report_result.get("data", {})

        new_leads = report.get("new_leads", 0)
        pending_followups = report.get("pending_followups", 0)
        pending_orders = report.get("pending_orders", 0)
        delayed_projects = report.get("delayed_projects", 0)
        employees_on_leave = report.get("employees_on_leave", 0)

        return {
            "agent": self.name,
            "status": "success",
            "data": report,
            "message": (
                "Today's BO report: "
                f"{new_leads} new leads, "
                f"{pending_followups} pending sales follow-ups, "
                f"{pending_orders} pending orders, "
                f"{delayed_projects} delayed projects, "
                f"and {employees_on_leave} employees on leave."
            ),
        }
