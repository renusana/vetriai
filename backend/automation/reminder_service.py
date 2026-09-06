from tools.crm_tool import CRMTool
from tools.project_tool import ProjectTool
from notifications.utils import create_notification


class ReminderService:
    """
    Generates automated reminders from existing business data.
    """

    def __init__(self):
        self.crm_tool = CRMTool()
        self.project_tool = ProjectTool()

    def generate_reminders(self, user):
        """
        Check business data and create reminders
        for the logged-in user.
        """

        reminders = []

        # ==========================================
        # Pending Sales Follow-ups
        # ==========================================

        followup_result = self.crm_tool.execute(
            "get_pending_followups",
            user=user,
        )

        if followup_result.get("status") == "success":

            followups = followup_result.get("data", {}).get("pending_followups", [])

            for followup in followups:

                customer = followup.get(
                    "customer",
                    "Customer",
                )

                days_pending = followup.get(
                    "days_pending",
                    0,
                )

                notification = create_notification(
                    user=user,
                    notification_type="high_priority_lead",
                    title="Sales Follow-up Reminder",
                    message=(
                        f"Follow-up is pending for "
                        f"{customer} for "
                        f"{days_pending} days."
                    ),
                    priority="high",
                    channel="in_app",
                    related_id=customer,
                )

                reminders.append(notification)

        # ==========================================
        # Pending Project Tasks
        # ==========================================

        task_result = self.project_tool.execute(
            "get_project_tasks",
            user=user,
        )

        if task_result.get("status") == "success":

            tasks = task_result.get("data", {}).get("tasks", [])

            for task in tasks:

                if task.get("status") == "Completed":
                    continue

                project = task.get(
                    "project",
                    "Project",
                )

                task_name = task.get(
                    "task",
                    "Task",
                )

                notification = create_notification(
                    user=user,
                    notification_type="critical_project_risk",
                    title="Pending Project Task",
                    message=(
                        f"Task '{task_name}' "
                        f"for project '{project}' "
                        f"is still pending."
                    ),
                    priority="high",
                    channel="in_app",
                    related_id=project,
                )

                reminders.append(notification)

        # ==========================================
        # Upcoming Project Deadlines
        # ==========================================

        deadline_result = self.project_tool.execute(
            "get_project_deadlines",
            user=user,
        )

        if deadline_result.get("status") == "success":

            deadlines = deadline_result.get("data", {}).get("deadlines", [])

            for deadline in deadlines:

                project = deadline.get(
                    "project",
                    "Project",
                )

                deadline_date = deadline.get(
                    "deadline",
                    "Unknown",
                )

                notification = create_notification(
                    user=user,
                    notification_type="deadline_approaching",
                    title="Project Deadline Reminder",
                    message=(
                        f"Project '{project}' "
                        f"has a deadline on "
                        f"{deadline_date}."
                    ),
                    priority="high",
                    channel="in_app",
                    related_id=project,
                )

                reminders.append(notification)

        # ==========================================
        # Pending Orders
        # ==========================================

        order_result = self.crm_tool.execute(
            "get_pending_orders",
            user=user,
        )

        if order_result.get("status") == "success":

            orders = order_result.get("data", {}).get("orders", [])

            for order in orders:

                order_id = order.get(
                    "order_id",
                    "Order",
                )

                customer = order.get(
                    "customer",
                    "Customer",
                )

                notification = create_notification(
                    user=user,
                    notification_type="important_customer_issue",
                    title="Pending Order Reminder",
                    message=(
                        f"Order {order_id} " f"for {customer} " f"is still pending."
                    ),
                    priority="medium",
                    channel="in_app",
                    related_id=order_id,
                )

                reminders.append(notification)

        return {
            "status": "success",
            "total_reminders": len(reminders),
            "message": (f"{len(reminders)} automated " f"reminders generated."),
        }
