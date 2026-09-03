from .base_agent import BaseAgent
from tools.finance_tool import FinanceTool


class FinanceAgent(BaseAgent):

    name = "Finance Agent"

    description = "Handles finance and financial summary questions"

    def __init__(self):
        self.finance_tool = FinanceTool()

    def can_handle(self, request):

        finance_keywords = [
            "finance",
            "financial",
            "revenue",
            "expense",
            "expenses",
            "profit",
            "financial summary",
        ]

        request_lower = request.lower()

        return any(keyword in request_lower for keyword in finance_keywords)

    def get_required_permission(self, request):

        return "view_finance"

    def process(self, request, user, credentials=None):

        request_lower = request.lower()

        if (
            "finance" in request_lower
            or "financial" in request_lower
            or "revenue" in request_lower
            or "expense" in request_lower
            or "expenses" in request_lower
            or "profit" in request_lower
            or "summary" in request_lower
        ):

            result = self.finance_tool.execute(
                "get_finance_summary",
                user,
            )

            if result.get("status") == "success":

                data = result.get("data", {})

                message = (
                    "Finance Summary:\n"
                    f"Total Revenue: {data.get('total_revenue', 0)}\n"
                    f"Total Expenses: {data.get('total_expenses', 0)}\n"
                    f"Net Profit: {data.get('net_profit', 0)}"
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
            "message": "The requested finance information is not currently supported.",
        }
