from .base_agent import BaseAgent


class MarketingAgent(BaseAgent):

    name = "Marketing Agent"

    description = (
        "Handles marketing, campaigns, leads, and marketing performance questions"
    )

    def can_handle(self, request):

        marketing_keywords = [
            "marketing",
            "campaign",
            "campaigns",
            "advertising",
            "advertisement",
            "promotion",
            "promotions",
            "marketing performance",
            "marketing summary",
            "conversion",
            "clicks",
            "impressions",
        ]

        request_lower = request.lower()

        return any(keyword in request_lower for keyword in marketing_keywords)

    def get_required_permission(self, request):

        return "view_marketing"

    def process(self, request, user, credentials=None):

        request_lower = request.lower()

        if (
            "marketing" in request_lower
            or "campaign" in request_lower
            or "advertising" in request_lower
            or "promotion" in request_lower
            or "conversion" in request_lower
            or "clicks" in request_lower
            or "impressions" in request_lower
        ):

            data = {
                "total_campaigns": 12,
                "active_campaigns": 5,
                "total_leads": 350,
                "conversions": 75,
            }

            message = (
                "Marketing Summary:\n"
                f"Total Campaigns: {data['total_campaigns']}\n"
                f"Active Campaigns: {data['active_campaigns']}\n"
                f"Total Leads: {data['total_leads']}\n"
                f"Conversions: {data['conversions']}"
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
            "message": "The requested marketing information is not currently supported.",
        }
