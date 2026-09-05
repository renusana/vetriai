from .base_agent import BaseAgent


class CustomerSupportAgent(BaseAgent):

    name = "Customer Support Agent"

    description = (
        "Handles customer support, customer issues, complaints, "
        "follow-ups, and support information"
    )

    def can_handle(self, request):

        support_keywords = [
            "customer support",
            "customer service",
            "support",
            "customer issue",
            "customer issues",
            "complaint",
            "complaints",
            "ticket",
            "tickets",
            "support request",
            "support requests",
            "customer problem",
            "customer problems",
            "customer complaint",
        ]

        request_lower = request.lower()

        return any(keyword in request_lower for keyword in support_keywords)

    def get_required_permission(self, request):

        return "view_customer_support"

    def process(self, request, user, credentials=None):

        request_lower = request.lower()

        if any(
            keyword in request_lower
            for keyword in [
                "customer support",
                "customer service",
                "support",
                "customer issue",
                "customer issues",
                "complaint",
                "complaints",
                "ticket",
                "tickets",
                "support request",
                "support requests",
                "customer problem",
                "customer problems",
                "customer complaint",
            ]
        ):

            data = {
                "total_customers": 3,
                "open_issues": 4,
                "pending_requests": 3,
                "resolved_issues": 18,
            }

            message = (
                "Customer Support Summary:\n"
                f"Total Customers: {data['total_customers']}\n"
                f"Open Issues: {data['open_issues']}\n"
                f"Pending Requests: {data['pending_requests']}\n"
                f"Resolved Issues: {data['resolved_issues']}"
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
            "message": (
                "The requested customer support information "
                "is not currently supported."
            ),
        }
