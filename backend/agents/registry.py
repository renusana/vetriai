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
        ]

    def get_agents(self):
        return self.agents

    def find_agent(self, request):
        """
        Return the best matching agent.
        """

        print("USER REQUEST:", request)

        request_lower = request.lower()

        # -------------------------------------------------
        # HR-specific priority
        # -------------------------------------------------

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

                    print("SELECTED AGENT:", agent.name)

                    return agent

        # -------------------------------------------------
        # Reporting-specific priority
        # -------------------------------------------------

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

                    print("SELECTED AGENT:", agent.name)

                    return agent

        # -------------------------------------------------
        # GitHub-specific priority
        # -------------------------------------------------

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

                    print("SELECTED AGENT:", agent.name)

                    return agent

        # -------------------------------------------------
        # Normal agent routing
        # -------------------------------------------------

        for agent in self.agents:

            print("CHECKING AGENT:", agent.name)

            if agent.can_handle(request):

                print("SELECTED AGENT:", agent.name)

                return agent

        print("NO AGENT FOUND")

        return None

    def find_agents(self, request):
        """
        Return all agents that can handle the request.
        """

        print("USER REQUEST:", request)

        matched_agents = []

        for agent in self.agents:

            print("CHECKING AGENT:", agent.name)

            if agent.can_handle(request):

                print("MATCHED AGENT:", agent.name)

                matched_agents.append(agent)

        if not matched_agents:

            print("NO AGENTS FOUND")

        return matched_agents
