from .operations_agent import OperationsAgent
from .qa_agent import QAAgent
from .developer_agent import DeveloperAgent
from .marketing_agent import MarketingAgent
from .finance_agent import FinanceAgent
from .github_agent import GitHubAgent
from .hr_agent import HRAgent
from .sales_agent import SalesAgent
from .project_agent import ProjectAgent
from .reporting_agent import ReportingAgent
from .calendar_agent import CalendarAgent
from .customer_support_agent import CustomerSupportAgent
from .cloud_storage_agent import CloudStorageAgent


class AgentRegistry:
    """
    Registry containing all available AI agents.
    """

    def __init__(self):

        self.agents = [
            CalendarAgent(),
            HRAgent(),
            SalesAgent(),
            ProjectAgent(),
            FinanceAgent(),
            MarketingAgent(),
            DeveloperAgent(),
            CustomerSupportAgent(),
            QAAgent(),
            OperationsAgent(),
            ReportingAgent(),
            GitHubAgent(),
            CloudStorageAgent(),
        ]

    # =========================================================
    # Get All Agents
    # =========================================================

    def get_agents(self):

        return self.agents

    # =========================================================
    # Find Single Best Agent
    # =========================================================

    def find_agent(self, request):
        """
        Return the best matching single agent.

        This method is intentionally preserved for normal
        single-agent requests.
        """

        print("USER REQUEST:", request)

        request_lower = request.lower()

        # -----------------------------------------------------
        # HR-specific priority
        # -----------------------------------------------------

        hr_keywords = [
            "reporting manager",
            "who is the reporting manager",
            "planned leave",
            "emergency leave",
            "work from home",
            "wfh",
            "hr policy",
            "leave policy",
            "employee policy",
        ]

        if any(keyword in request_lower for keyword in hr_keywords):

            for agent in self.agents:

                if agent.name == "HR Agent":

                    print(
                        "SELECTED AGENT:",
                        agent.name,
                    )

                    return agent

        # -----------------------------------------------------
        # Reporting-specific priority
        # -----------------------------------------------------

        reporting_keywords = [
            "report",
            "reports",
            "reporting",
            "business report",
            "business reports",
            "business reporting",
            "business summary",
            "business performance",
            "overall business",
            "overall business performance",
            "overall business report",
            "bo report",
            "daily report",
            "generate report",
            "generate a report",
            "show report",
            "show me the report",
            "report summary",
            "reporting summary",
        ]

        if any(keyword in request_lower for keyword in reporting_keywords):

            for agent in self.agents:

                if agent.name == "Reporting Agent":

                    print(
                        "SELECTED AGENT:",
                        agent.name,
                    )

                    return agent

        # -----------------------------------------------------
        # GitHub-specific priority
        # -----------------------------------------------------

        github_keywords = [
            "github",
            "git",
            "repository",
            "repositories",
            "repo",
            "repos",
            "pull request",
            "pull requests",
            "git status",
            "repository status",
        ]

        if any(keyword in request_lower for keyword in github_keywords):

            for agent in self.agents:

                if agent.name == "GitHub Agent":

                    print(
                        "SELECTED AGENT:",
                        agent.name,
                    )

                    return agent

        # -----------------------------------------------------
        # Customer Support-specific priority
        # -----------------------------------------------------

        customer_support_keywords = [
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

        if any(keyword in request_lower for keyword in customer_support_keywords):

            for agent in self.agents:

                if agent.name == "Customer Support Agent":

                    print(
                        "SELECTED AGENT:",
                        agent.name,
                    )

                    return agent

        # -----------------------------------------------------
        # Cloud Storage priority
        # -----------------------------------------------------

        cloud_storage_keywords = [
            "cloud storage",
            "storage summary",
            "storage usage",
            "cloud files",
            "cloud documents",
            "recent files",
        ]

        if any(keyword in request_lower for keyword in cloud_storage_keywords):

            for agent in self.agents:

                if agent.name == "Cloud Storage Agent":

                    print(
                        "SELECTED AGENT:",
                        agent.name,
                    )

                    return agent

        # -----------------------------------------------------
        # Normal Agent Routing
        # -----------------------------------------------------

        for agent in self.agents:

            print(
                "CHECKING AGENT:",
                agent.name,
            )

            if agent.can_handle(request):

                print(
                    "SELECTED AGENT:",
                    agent.name,
                )

                return agent

        print("NO AGENT FOUND")

        return None

    # =========================================================
    # Find All Agents
    # =========================================================

    def find_agents(self, request):
        """
        Return all agents that can technically handle
        the request.

        This method is useful for multi-agent discovery.
        """

        print("USER REQUEST:", request)

        matched_agents = []

        for agent in self.agents:

            print(
                "CHECKING AGENT:",
                agent.name,
            )

            if agent.can_handle(request):

                print(
                    "MATCHED AGENT:",
                    agent.name,
                )

                matched_agents.append(agent)

        if not matched_agents:

            print("NO AGENTS FOUND")

        return matched_agents

    # =========================================================
    # Find Relevant Agents For Multi-Agent Requests
    # =========================================================

    def find_relevant_agents(self, request):
        """
        Identify agents that have meaningful domain-specific
        matches in the user's request.

        This avoids accidental matches caused by generic
        overlapping words such as 'customer' or 'revenue'.
        """

        print("========================================")
        print("FINDING RELEVANT MULTI-AGENTS")
        print("REQUEST:", request)
        print("========================================")

        request_lower = request.lower()

        matches = []

        # =====================================================
        # Sales
        # =====================================================

        sales_keywords = [
            "sales",
            "sale",
            "lead",
            "leads",
            "follow-up",
            "follow up",
            "followups",
            "order",
            "orders",
            "sales policy",
            "sales sop",
            "sales process",
        ]

        sales_score = sum(1 for keyword in sales_keywords if keyword in request_lower)

        # =====================================================
        # Finance
        # =====================================================

        finance_keywords = [
            "finance",
            "financial",
            "expense",
            "expenses",
            "profit",
            "financial summary",
        ]

        finance_score = sum(
            1 for keyword in finance_keywords if keyword in request_lower
        )

        # Revenue is shared between Sales and Finance.
        # It alone should not create a multi-agent request.
        if "revenue" in request_lower:

            if sales_score == 0 and finance_score == 0:
                finance_score = 1

        # =====================================================
        # Project
        # =====================================================

        project_keywords = [
            "project",
            "projects",
            "delayed",
            "delay",
            "deadline",
            "deadlines",
            "task",
            "tasks",
            "milestone",
            "milestones",
            "project status",
            "project policy",
            "project sop",
            "project process",
        ]

        project_score = sum(
            1 for keyword in project_keywords if keyword in request_lower
        )

        # =====================================================
        # GitHub
        # =====================================================

        github_keywords = [
            "github",
            "git",
            "repository",
            "repositories",
            "repo",
            "repos",
            "pull request",
            "pull requests",
            "git status",
            "repository status",
        ]

        github_score = sum(1 for keyword in github_keywords if keyword in request_lower)

        # =====================================================
        # Marketing
        # =====================================================

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

        marketing_score = sum(
            1 for keyword in marketing_keywords if keyword in request_lower
        )

        # =====================================================
        # Customer Support
        # =====================================================

        customer_support_keywords = [
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

        customer_support_score = sum(
            1 for keyword in customer_support_keywords if keyword in request_lower
        )

        # =====================================================
        # Calendar
        # =====================================================

        calendar_keywords = [
            "calendar",
            "event",
            "events",
            "meeting",
            "meetings",
            "schedule",
            "scheduled",
            "appointment",
            "appointments",
        ]

        calendar_score = sum(
            1 for keyword in calendar_keywords if keyword in request_lower
        )

        # =====================================================
        # Other Agents
        # =====================================================

        # These agents are included using their existing
        # can_handle() implementation.
        other_agents = [
            agent
            for agent in self.agents
            if agent.name
            not in [
                "Sales Agent",
                "Finance Agent",
                "Project Agent",
                "GitHub Agent",
                "Marketing Agent",
                "Customer Support Agent",
                "Calendar Agent",
            ]
        ]

        # =====================================================
        # Build Score Map
        # =====================================================

        scores = {
            "Sales Agent": sales_score,
            "Finance Agent": finance_score,
            "Project Agent": project_score,
            "GitHub Agent": github_score,
            "Marketing Agent": marketing_score,
            "Customer Support Agent": customer_support_score,
            "Calendar Agent": calendar_score,
        }

        # =====================================================
        # Add Strong Matches
        # =====================================================

        for agent in self.agents:

            score = scores.get(
                agent.name,
                0,
            )

            if score > 0:

                print(
                    "RELEVANT AGENT:",
                    agent.name,
                    "SCORE:",
                    score,
                )

                matches.append((agent, score))

        # =====================================================
        # Add Other Agents
        # =====================================================

        for agent in other_agents:

            if agent.can_handle(request):

                print(
                    "RELEVANT AGENT:",
                    agent.name,
                    "SCORE:",
                    1,
                )

                matches.append((agent, 1))

        # =====================================================
        # Sort By Score
        # =====================================================

        matches.sort(
            key=lambda item: item[1],
            reverse=True,
        )

        selected_agents = [agent for agent, score in matches]

        print(
            "FINAL RELEVANT AGENTS:",
            [agent.name for agent in selected_agents],
        )

        return selected_agents
