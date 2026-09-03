from .models import AuditLog


def create_audit_log(
    user,
    agent,
    request,
    data_accessed="",
    tool="",
    action="",
    approval="",
    result="",
):
    return AuditLog.objects.create(
        user=user,
        agent=agent,
        request=request,
        data_accessed=data_accessed,
        tool=tool,
        action=action,
        approval=approval,
        result=result,
    )
