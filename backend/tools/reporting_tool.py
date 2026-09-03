class ReportingTool:
    """
    Controlled tool for generating business reports.
    """

    name = "reporting_tool"
    description = "Generates approved business reports."

    def execute(self, action, user=None):

        if action == "generate_daily_report":

            return {
                "status": "success",
                "data": {
                    "new_leads": 12,
                    "pending_followups": 5,
                    "pending_orders": 3,
                    "delayed_projects": 2,
                    "employees_on_leave": 2,
                },
            }

        return {"status": "error", "message": "Reporting action not supported."}
