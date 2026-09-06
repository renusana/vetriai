from tools.crm_tool import CRMTool
from tools.project_tool import ProjectTool
from notifications.models import Notification
from notifications.utils import create_notification


class ReminderService:
    """
    Generates automated reminders from existing business data.
    Prevents duplicate reminders for the same user and business item.
    """

    def __init__(self):
        self.crm_tool = CRMTool()
        self.project_tool = ProjectTool()

    def create_reminder_if_not_exists(
        self,
        user,
        notification_type,
        title,
        message,
        priority,
        related_id,
    ):
        """
        Create a reminder only if the same reminder
        does not already exist for the user.
        """

        existing_notification = Notification.objects.filter(
            user=user,
            notification_type=notification_type,
            related_id=related_id,
            is_read=False,
        ).first()

        if existing_notification:
            return None

        return create_notification(
            user=user,
            notification_type=notification_type,
            title=title,
            message=message,
            priority=priority,
            channel="in_app",
            related_id=related_id,
        )

    def generate_reminders(self, user):

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

                notification = self.create_reminder_if_not_exists(
                    user=user,
                    notification_type="high_priority_lead",
                    title="Sales Follow-up Reminder",
                    message=(
                        f"Follow-up is pending for "
                        f"{customer} for "
                        f"{days_pending} days."
                    ),
                    priority="high",
                    related_id=customer,
                )

                if notification:
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

                # Use project + task so different tasks
                # in the same project don't conflict.
                related_id = f"{project}:{task_name}"

                notification = self.create_reminder_if_not_exists(
                    user=user,
                    notification_type="critical_project_risk",
                    title="Pending Project Task",
                    message=(
                        f"Task '{task_name}' "
                        f"for project '{project}' "
                        f"is still pending."
                    ),
                    priority="high",
                    related_id=related_id,
                )

                if notification:
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

                # Include date so a future deadline
                # can generate a new reminder.
                related_id = f"{project}:{deadline_date}"

                notification = self.create_reminder_if_not_exists(
                    user=user,
                    notification_type="deadline_approaching",
                    title="Project Deadline Reminder",
                    message=(
                        f"Project '{project}' "
                        f"has a deadline on "
                        f"{deadline_date}."
                    ),
                    priority="high",
                    related_id=related_id,
                )

                if notification:
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

                notification = self.create_reminder_if_not_exists(
                    user=user,
                    notification_type="important_customer_issue",
                    title="Pending Order Reminder",
                    message=(
                        f"Order {order_id} " f"for {customer} " f"is still pending."
                    ),
                    priority="medium",
                    related_id=order_id,
                )

                if notification:
                    reminders.append(notification)

        return {
            "status": "success",
            "total_reminders": len(reminders),
            "message": (f"{len(reminders)} new automated " f"reminders generated."),
        }
