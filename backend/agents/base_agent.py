from abc import ABC, abstractmethod


class BaseAgent(ABC):
    """
    Base class for all AI agents.
    """

    name = "Base Agent"
    description = "Base agent for Vetri AI Multi-Agent system"

    @abstractmethod
    def can_handle(self, request):
        """
        Determines whether this agent can handle the request.
        """
        pass

    @abstractmethod
    def process(self, request, user, credentials=None):
        """
        Processes the user request.
        """
        pass
