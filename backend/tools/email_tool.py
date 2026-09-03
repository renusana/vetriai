from django.core.mail import send_mail


class EmailTool:
    """
    Controlled tool for email-related operations.

    Sends email only when the action reaches the tool execution stage.
    Approval is handled separately by ApprovalWorkflow.
    """

    name = "email_tool"
    description = "Handles approved email operations."

    def execute(
        self,
        action,
        user=None,
        recipient=None,
        subject=None,
        message=None,
    ):
        if action != "send_email":
            return {
                "status": "error",
                "message": "Email action not supported.",
            }

        if not recipient:
            return {
                "status": "error",
                "message": "Recipient is required.",
            }

        if not subject:
            return {
                "status": "error",
                "message": "Subject is required.",
            }

        if not message:
            return {
                "status": "error",
                "message": "Message is required.",
            }

        try:
            sent_count = send_mail(
                subject=subject,
                message=message,
                from_email=None,
                recipient_list=[recipient],
                fail_silently=False,
            )

            if sent_count == 1:
                return {
                    "status": "success",
                    "message": f"Email sent successfully to {recipient}.",
                    "recipient": recipient,
                    "subject": subject,
                }

            return {
                "status": "error",
                "message": "Email was not sent.",
            }

        except Exception as e:
            return {
                "status": "error",
                "message": f"Email sending failed: {str(e)}",
            }
