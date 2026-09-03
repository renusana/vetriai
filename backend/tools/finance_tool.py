class FinanceTool:
    """
    Controlled tool for finance-related operations.

    Real finance/database integration can be added later.
    """

    name = "finance_tool"
    description = "Provides controlled finance information."

    def execute(self, action, user=None):

        if action == "get_finance_summary":

            return {
                "status": "success",
                "data": {
                    "total_revenue": 125000,
                    "total_expenses": 75000,
                    "net_profit": 50000,
                },
            }

        return {
            "status": "error",
            "message": "Finance action not supported.",
        }
