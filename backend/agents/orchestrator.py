from .registry import AgentRegistry
from permissions.permission_engine import PermissionEngine
from audit_logs.utils import create_audit_log


class AIOrchestrator:
    """
    Central coordinator for the Vetri AI Multi-Agent system.
    """

    def __init__(self):

        self.registry = AgentRegistry()
        self.permission_engine = PermissionEngine()

    def get_available_agents(self):

        return [
            {
                "name": agent.name,
                "description": agent.description,
            }
            for agent in self.registry.get_agents()
        ]

    def understand_intent(self, request):

        agent = self.registry.find_agent(request)

        if agent:

            return {
                "intent": agent.name,
                "agent": agent,
            }

        return {
            "intent": "unknown",
            "agent": None,
        }

    # =========================================================
    # Management / Business Priority Detection
    # =========================================================

    def is_management_query(self, request):

        management_keywords = [
            "business priorities",
            "business priority",
            "important business",
            "important priorities",
            "important priority",
            "management priorities",
            "management priority",
            "business overview",
            "management overview",
            "what is important",
            "what's important",
            "what needs attention",
            "what should i focus on",
            "what should we focus on",
            "priorities for tomorrow",
            "important for tomorrow",
        ]

        request_lower = request.lower()

        return any(keyword in request_lower for keyword in management_keywords)

    # =========================================================
    # Knowledge / Policy Detection
    # =========================================================

    def is_knowledge_question(self, request):

        knowledge_keywords = [
            "policy",
            "how can",
            "how do",
            "how many days",
            "who approves",
            "work from home",
            "wfh",
            "planned leave",
            "emergency leave",
            "reporting manager",
        ]

        request_lower = request.lower()

        return any(keyword in request_lower for keyword in knowledge_keywords)

    # =========================================================
    # Process Management Query
    # =========================================================

    def process_management_query(
        self,
        request,
        user,
        role="employee",
        credentials=None,
    ):
        """
        Coordinate multiple business agents for management
        and business-priority questions.
        """

        print("========================================")
        print("MULTI-AGENT MANAGEMENT QUERY")
        print("REQUEST:", request)
        print("========================================")

        # -----------------------------------------------------
        # Agents participating in management overview
        # -----------------------------------------------------

        agent_names = [
            "HR Agent",
            "Project Agent",
            "Sales Agent",
            "Finance Agent",
            "Calendar Agent",
        ]

        # -----------------------------------------------------
        # Agent-specific requests
        # -----------------------------------------------------

        agent_requests = {
            "HR Agent": "Which employees are on leave tomorrow?",
            "Project Agent": "What are the upcoming project deadlines?",
            "Sales Agent": "What customer follow-ups are pending?",
            "Finance Agent": "Show the finance summary.",
            "Calendar Agent": "What meetings and events are scheduled tomorrow?",
        }

        all_agents = self.registry.get_agents()

        selected_agents = [agent for agent in all_agents if agent.name in agent_names]

        results = []

        # =====================================================
        # Run Selected Agents
        # =====================================================

        for agent in selected_agents:

            print("RUNNING AGENT:", agent.name)

            # -------------------------------------------------
            # Get permission required by the agent
            # -------------------------------------------------

            required_permission = None

            if hasattr(agent, "get_required_permission"):

                required_permission = agent.get_required_permission(
                    agent_requests.get(
                        agent.name,
                        request,
                    )
                )

            # -------------------------------------------------
            # Permission check
            # -------------------------------------------------

            if required_permission:

                permission_result = self.permission_engine.check_permission(
                    role,
                    required_permission,
                )

                if not permission_result["allowed"]:

                    print(
                        "PERMISSION DENIED:",
                        agent.name,
                        required_permission,
                    )

                    results.append(
                        {
                            "agent": agent.name,
                            "status": "denied",
                            "data": {},
                            "message": (
                                f"{agent.name} information "
                                "is not available for your role."
                            ),
                        }
                    )

                    continue

            # -------------------------------------------------
            # Agent-specific request
            # -------------------------------------------------

            agent_request = agent_requests.get(
                agent.name,
                request,
            )

            print(
                "AGENT REQUEST:",
                agent_request,
            )

            # -------------------------------------------------
            # Execute agent
            # -------------------------------------------------

            try:

                # Calendar Agent requires Google credentials
                if agent.name == "Calendar Agent":

                    agent_result = agent.process(
                        agent_request,
                        user,
                        credentials=credentials,
                    )

                # All other agents do not require credentials
                else:

                    agent_result = agent.process(
                        agent_request,
                        user,
                    )

                results.append(agent_result)

            except Exception as error:

                print(
                    f"ERROR FROM {agent.name}:",
                    str(error),
                )

                results.append(
                    {
                        "agent": agent.name,
                        "status": "error",
                        "data": {},
                        "message": (
                            f"{agent.name} could not retrieve "
                            "the requested information."
                        ),
                    }
                )

        # =====================================================
        # Combine Agent Results
        # =====================================================

        successful_results = [
            result for result in results if result.get("status") == "success"
        ]

        if not successful_results:

            response_message = (
                "I could not retrieve the required business "
                "information from the available agents."
            )

        else:

            response_sections = []

            for result in successful_results:

                agent_name = result.get(
                    "agent",
                    "Business Agent",
                )

                message = result.get(
                    "message",
                    "",
                )

                if message:

                    response_sections.append(f"{agent_name}:\n{message}")

            response_message = "Business Priority Overview:\n\n" + "\n\n".join(
                response_sections
            )

        # =====================================================
        # Audit Log
        # =====================================================

        create_audit_log(
            user=user,
            agent="Multi-Agent Orchestrator",
            request=request,
            action="Multi-agent business priority analysis",
            approval="Not required",
            result=response_message,
        )

        # =====================================================
        # Return
        # =====================================================

        return {
            "status": "success",
            "intent": "multi_agent_management",
            "agent": "Multi-Agent Orchestrator",
            "response": response_message,
            "data": {
                "agent_results": results,
            },
        }

    # =========================================================
    # Main Request Processor
    # =========================================================

    def process_request(
        self,
        request,
        user,
        role="employee",
        permission=None,
        credentials=None,
    ):

        # =====================================================
        # Step 1: Management / Multi-Agent Query
        # =====================================================

        if self.is_management_query(request):

            return self.process_management_query(
                request=request,
                user=user,
                role=role,
                credentials=credentials,
            )

        # =====================================================
        # Step 2: Understand Intent
        # =====================================================

        intent_result = self.understand_intent(request)

        agent = intent_result["agent"]

        is_knowledge_question = self.is_knowledge_question(request)

        # =====================================================
        # Step 3: No Agent Found
        # =====================================================

        if agent is None:

            response_message = (
                "I'm not sure which business area " "can handle your request yet."
            )

            create_audit_log(
                user=user,
                agent="Unknown",
                request=request,
                action="Intent identification",
                approval="Not required",
                result=response_message,
            )

            return {
                "status": "success",
                "intent": "unknown",
                "agent": None,
                "response": response_message,
                "data": {},
            }

        # =====================================================
        # Step 4: Permission Check
        # =====================================================

        required_permission = permission

        if required_permission is None and hasattr(agent, "get_required_permission"):

            required_permission = agent.get_required_permission(request)

        if required_permission and not is_knowledge_question:

            permission_result = self.permission_engine.check_permission(
                role,
                required_permission,
            )

            if not permission_result["allowed"]:

                response_message = (
                    "You do not have permission " "to perform this action."
                )

                create_audit_log(
                    user=user,
                    agent=agent.name,
                    request=request,
                    action="Permission check",
                    approval="Denied",
                    result="Denied: " + response_message,
                )

                return {
                    "status": "denied",
                    "intent": intent_result["intent"],
                    "agent": agent.name,
                    "response": response_message,
                    "data": {},
                }

        # =====================================================
        # Step 5: Agent Processing
        # =====================================================

        try:

            # Calendar Agent requires Google credentials
            if agent.name == "Calendar Agent":

                agent_result = agent.process(
                    request,
                    user,
                    credentials=credentials,
                )

            # All other agents do not require credentials
            else:

                agent_result = agent.process(
                    request,
                    user,
                )

        except Exception as error:

            print(
                f"ERROR FROM {agent.name}:",
                str(error),
            )

            response_message = (
                "The requested operation could not be " "completed safely."
            )

            create_audit_log(
                user=user,
                agent=agent.name,
                request=request,
                action="Agent processing",
                approval="Not required",
                result=response_message,
            )

            return {
                "status": "error",
                "intent": intent_result["intent"],
                "agent": agent.name,
                "response": response_message,
                "data": {},
            }

        # =====================================================
        # Step 6: Audit Log
        # =====================================================

        create_audit_log(
            user=user,
            agent=agent.name,
            request=request,
            data_accessed=str(agent_result.get("data", {})),
            action="Process user request",
            approval="Not required",
            result=agent_result.get(
                "message",
                "",
            ),
        )

        # =====================================================
        # Step 7: Return Result
        # =====================================================

        return {
            "status": "success",
            "intent": intent_result["intent"],
            "agent": agent.name,
            "response": agent_result["message"],
            "data": agent_result["data"],
        }
