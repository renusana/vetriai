from tools.crm_tool import CRMTool
from tools.project_tool import ProjectTool
from tools.database_tool import DatabaseTool


class ReportingTool:
    """
    Controlled tool for generating business reports.
    """

    name = "reporting_tool"
    description = "Generates approved business reports."

    def execute(self, action, user=None):

        if action == "generate_daily_report":

            crm_tool = CRMTool()
            project_tool = ProjectTool()
            database_tool = DatabaseTool()

            # Get current business data from existing tools
            leads = crm_tool.execute("get_leads", user=user)

            followups = crm_tool.execute("get_pending_followups", user=user)

            pending_orders = crm_tool.execute("get_pending_orders", user=user)

            delayed_projects = project_tool.execute("get_delayed_projects", user=user)

            employees_on_leave = database_tool.execute(
                "get_employees_on_leave", user=user
            )

            # Extract report values
            leads_data = leads.get("data", {})
            followups_data = followups.get("data", {})
            orders_data = pending_orders.get("data", {})
            projects_data = delayed_projects.get("data", {})
            leave_data = employees_on_leave.get("data", {})

            report = {
                "new_leads": leads_data.get("new_leads", 0),
                "pending_followups": len(followups_data.get("pending_followups", [])),
                "pending_orders": orders_data.get("pending_orders", 0),
                "delayed_projects": projects_data.get("total_delayed", 0),
                "employees_on_leave": leave_data.get("total_on_leave", 0),
            }

            return {
                "status": "success",
                "data": report,
            }

        return {"status": "error", "message": "Reporting action not supported."}
