from .models import Notification


def create_notification(
    user,
    notification_type,
    title,
    message,
    priority="medium",
    channel="in_app",
    related_id=None,
):
    """
    Create a notification for a user.
    """

    return Notification.objects.create(
        user=user,
        notification_type=notification_type,
        title=title,
        message=message,
        priority=priority,
        channel=channel,
        related_id=related_id,
    )


def create_project_risk_notification(
    user,
    message,
    related_id=None,
):
    """
    Create a notification for a critical project risk.
    """

    return create_notification(
        user=user,
        notification_type="critical_project_risk",
        title="Critical Project Risk",
        message=message,
        priority="critical",
        channel="in_app",
        related_id=related_id,
    )


def create_high_priority_lead_notification(
    user,
    message,
    related_id=None,
):
    """
    Create a notification for a high-priority lead.
    """

    return create_notification(
        user=user,
        notification_type="high_priority_lead",
        title="High-Priority Lead",
        message=message,
        priority="high",
        channel="in_app",
        related_id=related_id,
    )


def create_overdue_payment_notification(
    user,
    message,
    related_id=None,
):
    """
    Create a notification for an overdue payment.
    """

    return create_notification(
        user=user,
        notification_type="overdue_payment",
        title="Overdue Payment",
        message=message,
        priority="high",
        channel="in_app",
        related_id=related_id,
    )


def create_customer_issue_notification(
    user,
    message,
    related_id=None,
):
    """
    Create a notification for an important customer issue.
    """

    return create_notification(
        user=user,
        notification_type="important_customer_issue",
        title="Important Customer Issue",
        message=message,
        priority="high",
        channel="in_app",
        related_id=related_id,
    )


def create_approval_pending_notification(
    user,
    message,
    related_id=None,
    channel="in_app",
):
    """
    Create a notification for a pending approval.

    The channel can be:
    - in_app
    - email
    """

    return create_notification(
        user=user,
        notification_type="approval_pending",
        title="Approval Required",
        message=message,
        priority="high",
        channel=channel,
        related_id=related_id,
    )


def create_deadline_notification(
    user,
    message,
    related_id=None,
):
    """
    Create a notification for an approaching deadline.
    """

    return create_notification(
        user=user,
        notification_type="deadline_approaching",
        title="Deadline Approaching",
        message=message,
        priority="high",
        channel="in_app",
        related_id=related_id,
    )
