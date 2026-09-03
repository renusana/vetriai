import inspect

from .database_tool import DatabaseTool
from .email_tool import EmailTool
from .calendar_tool import CalendarTool
from .crm_tool import CRMTool
from .project_tool import ProjectTool
from .github_tool import GitHubTool
from .reporting_tool import ReportingTool

from approvals.approval_workflow import ApprovalWorkflow
from audit_logs.utils import create_audit_log


class ToolRegistry:
    """
    Central registry for all available tools.

    Agents can only access tools that are explicitly
    assigned to them.
    """

    def __init__(self):

        self.tools = {
            "database_tool": DatabaseTool(),
            "email_tool": EmailTool(),
            "calendar_tool": CalendarTool(),
            "crm_tool": CRMTool(),
            "project_tool": ProjectTool(),
            "github_tool": GitHubTool(),
            "reporting_tool": ReportingTool(),
        }

        self.approval_workflow = ApprovalWorkflow(executor=self.execute_approved_action)

        self.agent_permissions = {
            "Calendar Agent": {
                "calendar_tool",
            },
            "HR Agent": {
                "database_tool",
                "calendar_tool",
                "reporting_tool",
            },
            "Sales Agent": {
                "database_tool",
                "crm_tool",
                "email_tool",
                "calendar_tool",
            },
            "Project Agent": {
                "database_tool",
                "project_tool",
                "github_tool",
                "calendar_tool",
            },
            "Reporting Agent": {
                "database_tool",
                "reporting_tool",
            },
        }

    def get_tool(self, tool_name):
        """
        Get a registered tool by name.
        """

        return self.tools.get(tool_name)

    def get_allowed_tools(self, agent_name):
        """
        Get all tools allowed for a specific agent.
        """

        allowed_tool_names = self.agent_permissions.get(agent_name, set())

        return [self.tools[name] for name in allowed_tool_names]

    def is_allowed(self, agent_name, tool_name):
        """
        Check whether an agent is allowed to use a tool.
        """

        allowed_tools = self.agent_permissions.get(agent_name, set())

        return tool_name in allowed_tools

    def execute_tool(
        self,
        agent_name,
        tool_name,
        action,
        user=None,
        credentials=None,
    ):
        """
        Execute a tool only if the agent is authorized.
        """

        if not self.is_allowed(agent_name, tool_name):

            result = {
                "status": "denied",
                "message": (f"{agent_name} is not authorized " f"to use {tool_name}."),
            }

            create_audit_log(
                user=user or "Unknown",
                agent=agent_name,
                request=action,
                tool=tool_name,
                action=action,
                approval="Not required",
                result=result["message"],
            )

            return result

        tool = self.get_tool(tool_name)

        if tool is None:

            result = {
                "status": "error",
                "message": "Tool not found.",
            }

            create_audit_log(
                user=user or "Unknown",
                agent=agent_name,
                request=action,
                tool=tool_name,
                action=action,
                approval="Not required",
                result=result["message"],
            )

            return result

        result = tool.execute(action, user, credentials=credentials)

        create_audit_log(
            user=user or "Unknown",
            agent=agent_name,
            request=action,
            tool=tool_name,
            action=action,
            approval="Not required",
            result=str(result),
        )

        return result

    def execute_approved_action(
        self,
        agent_name,
        tool_name,
        action,
        parameters=None,
        user=None,
    ):
        """
        Execute an action after human approval.

        The agent must still be authorized to use the tool.
        """

        if parameters is None:
            parameters = {}

        if not self.is_allowed(agent_name, tool_name):

            result = {
                "status": "denied",
                "message": (f"{agent_name} is not authorized " f"to use {tool_name}."),
            }

            create_audit_log(
                user=user or "Unknown",
                agent=agent_name,
                request=action,
                tool=tool_name,
                action=action,
                approval="Approved - Execution Denied",
                result=result["message"],
            )

            return result

        tool = self.get_tool(tool_name)

        if tool is None:

            result = {
                "status": "error",
                "message": "Tool not found.",
            }

            create_audit_log(
                user=user or "Unknown",
                agent=agent_name,
                request=action,
                tool=tool_name,
                action=action,
                approval="Approved - Execution Failed",
                result=result["message"],
            )

            return result

        try:
            # Check which parameters the tool accepts.
            signature = inspect.signature(tool.execute)

            accepted_parameters = {
                key: value
                for key, value in parameters.items()
                if key in signature.parameters
            }

            result = tool.execute(
                action,
                user,
                **accepted_parameters,
            )

            create_audit_log(
                user=user or "Unknown",
                agent=agent_name,
                request=action,
                tool=tool_name,
                action=action,
                approval="Approved - Executed",
                result=str(result),
            )

            return result

        except Exception as exc:

            result = {
                "status": "error",
                "message": f"Approved action execution failed: {str(exc)}",
            }

            create_audit_log(
                user=user or "Unknown",
                agent=agent_name,
                request=action,
                tool=tool_name,
                action=action,
                approval="Approved - Execution Failed",
                result=result["message"],
            )

            return result

    def request_action(
        self,
        agent_name,
        tool_name,
        action,
        parameters=None,
        user=None,
    ):
        """
        Request execution of a tool action.

        Sensitive actions are sent to the approval workflow.
        """

        if not self.is_allowed(agent_name, tool_name):

            result = {
                "status": "denied",
                "message": (f"{agent_name} is not authorized " f"to use {tool_name}."),
            }

            create_audit_log(
                user=user or "Unknown",
                agent=agent_name,
                request=action,
                tool=tool_name,
                action=action,
                approval="Denied",
                result=result["message"],
            )

            return result

        if self.approval_workflow.requires_approval(action):

            return self.approval_workflow.create_action_preview(
                agent_name,
                tool_name,
                action,
                parameters,
                user=user,
            )

        result = {
            "status": "ready",
            "message": "Action can be executed.",
            "agent": agent_name,
            "tool": tool_name,
            "action": action,
            "parameters": parameters or {},
        }

        create_audit_log(
            user=user or "Unknown",
            agent=agent_name,
            request=action,
            tool=tool_name,
            action=action,
            approval="Not required",
            result=result["message"],
        )

        return result
