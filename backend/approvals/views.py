from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from tools.registry import ToolRegistry

# Single shared registry instance.
# This preserves pending_actions between API requests
# while the Django process is running.
tool_registry = ToolRegistry()


class ApprovalListView(APIView):
    """
    Get all approval actions.

    Optionally filter to only pending actions using:
    ?status=pending
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        actions = list(tool_registry.approval_workflow.pending_actions.values())

        status_filter = request.query_params.get("status")

        if status_filter:
            actions = [
                action for action in actions if action.get("status") == status_filter
            ]

        return Response(
            {
                "status": "success",
                "actions": actions,
                "count": len(actions),
            },
            status=status.HTTP_200_OK,
        )


class ApprovalPreviewView(APIView):
    """
    Create a sensitive action preview requiring human approval.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        agent_name = request.data.get("agent_name")
        tool_name = request.data.get("tool_name")
        action = request.data.get("action")
        parameters = request.data.get("parameters", {})

        if not agent_name or not tool_name or not action:
            return Response(
                {
                    "status": "error",
                    "message": ("agent_name, tool_name and action are required."),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not isinstance(parameters, dict):
            return Response(
                {
                    "status": "error",
                    "message": "parameters must be a JSON object.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        result = tool_registry.request_action(
            agent_name=agent_name,
            tool_name=tool_name,
            action=action,
            parameters=parameters,
            user=request.user,
        )

        return Response(result, status=status.HTTP_200_OK)


class ApprovalDetailView(APIView):
    """
    Get the current state of a pending action.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, action_id):
        action = tool_registry.approval_workflow.get_action(action_id)

        if action is None:
            return Response(
                {
                    "status": "error",
                    "message": "Action not found.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(
            {
                "status": "success",
                "action": action,
            },
            status=status.HTTP_200_OK,
        )


class ApprovalApproveView(APIView):
    """
    Approve and execute a pending action.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, action_id):
        result = tool_registry.approval_workflow.approve_action(
            action_id=action_id,
            user=request.user,
        )

        if result.get("status") == "error":
            return Response(
                result,
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            result,
            status=status.HTTP_200_OK,
        )


class ApprovalEditView(APIView):
    """
    Edit parameters of a pending action.
    """

    permission_classes = [IsAuthenticated]

    def put(self, request, action_id):
        updated_parameters = request.data.get(
            "parameters",
            {},
        )

        if not isinstance(updated_parameters, dict):
            return Response(
                {
                    "status": "error",
                    "message": "parameters must be a JSON object.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        result = tool_registry.approval_workflow.edit_action(
            action_id=action_id,
            updated_parameters=updated_parameters,
            user=request.user,
        )

        if result.get("status") == "error":
            return Response(
                result,
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            result,
            status=status.HTTP_200_OK,
        )


class ApprovalCancelView(APIView):
    """
    Cancel a pending action.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, action_id):
        result = tool_registry.approval_workflow.cancel_action(
            action_id=action_id,
            user=request.user,
        )

        if result.get("status") == "error":
            return Response(
                result,
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            result,
            status=status.HTTP_200_OK,
        )
