from tools.crm_tool import CRMTool
from tools.project_tool import ProjectTool
from tools.finance_tool import FinanceTool

from notifications.models import Notification
from notifications.utils import create_notification


class AlertService:
    """
    Generates intelligent business alerts from existing tools.

    Alerts are created only when a business condition
    requires attention.

    Duplicate alerts are prevented for the same user
    and business item.
    """

    def __init__(self):
        self.crm_tool = CRMTool()
        self.project_tool = ProjectTool()
        self.finance_tool = FinanceTool()

    # =========================================================
    # Duplicate Protection
    # =========================================================

    def create_alert_if_not_exists(
        self,
        user,
        notification_type,
        title,
        message,
        priority,
        related_id,
    ):
        """
        Creates an alert only when the same unread alert
        does not already exist.
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

    # =========================================================
    # Generate Intelligent Alerts
    # =========================================================

    def generate_alerts(self, user):

        alerts = []

        # =====================================================
        # 1. Critical Project Risk
        # =====================================================

        project_result = self.project_tool.execute(
            "get_delayed_projects",
            user=user,
        )

        if project_result.get("status") == "success":

            delayed_projects = project_result.get("data", {}).get(
                "delayed_projects", []
            )

            for project in delayed_projects:

                project_name = project.get(
                    "name",
                    "Project",
                )

                delay_days = project.get(
                    "delay_days",
                    0,
                )

                # Only generate a critical alert
                # when the project is actually delayed.
                if delay_days <= 0:
                    continue

                related_id = f"project-risk:{project_name}"

                notification = self.create_alert_if_not_exists(
                    user=user,
                    notification_type="critical_project_risk",
                    title="Critical Project Risk",
                    message=(
                        f"Project '{project_name}' "
                        f"is delayed by {delay_days} days "
                        f"and requires attention."
                    ),
                    priority="high",
                    related_id=related_id,
                )

                if notification:
                    alerts.append(notification)

        # =====================================================
        # 2. High-Priority Sales Follow-up
        # =====================================================

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

                # Consider follow-ups pending for
                # 7 or more days as high priority.
                if days_pending < 7:
                    continue

                related_id = f"lead-risk:{customer}"

                notification = self.create_alert_if_not_exists(
                    user=user,
                    notification_type="high_priority_lead",
                    title="High-Priority Lead Alert",
                    message=(
                        f"Follow-up for '{customer}' "
                        f"has been pending for "
                        f"{days_pending} days. "
                        f"Immediate attention is recommended."
                    ),
                    priority="high",
                    related_id=related_id,
                )

                if notification:
                    alerts.append(notification)

        # =====================================================
        # 3. High-Value Pending Order
        # =====================================================

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

                amount = order.get(
                    "amount",
                    0,
                )

                # Orders above 30,000 are considered
                # high-value pending orders.
                if amount <= 30000:
                    continue

                related_id = f"order-risk:{order_id}"

                notification = self.create_alert_if_not_exists(
                    user=user,
                    notification_type="important_customer_issue",
                    title="High-Value Pending Order",
                    message=(
                        f"Order {order_id} for {customer} "
                        f"is pending with a value of "
                        f"₹{amount:,}. "
                        f"Please review the order."
                    ),
                    priority="high",
                    related_id=related_id,
                )

                if notification:
                    alerts.append(notification)

        # =====================================================
        # 4. Finance Risk
        # =====================================================

        finance_result = self.finance_tool.execute(
            "get_finance_summary",
            user=user,
        )

        if finance_result.get("status") == "success":

            finance_data = finance_result.get(
                "data",
                {},
            )

            revenue = finance_data.get(
                "total_revenue",
                0,
            )

            expenses = finance_data.get(
                "total_expenses",
                0,
            )

            # Generate a finance alert when expenses
            # exceed revenue.
            if expenses > revenue:

                related_id = "finance-risk:expense"

                notification = self.create_alert_if_not_exists(
                    user=user,
                    notification_type="finance_risk",
                    title="Finance Risk Alert",
                    message=(
                        f"Total expenses (₹{expenses:,}) "
                        f"are higher than total revenue "
                        f"(₹{revenue:,}). "
                        f"Financial review is recommended."
                    ),
                    priority="high",
                    related_id=related_id,
                )

                if notification:
                    alerts.append(notification)

        # =====================================================
        # Final Response
        # =====================================================

        return {
            "status": "success",
            "total_alerts": len(alerts),
            "message": (f"{len(alerts)} new intelligent " f"alerts generated."),
        }
