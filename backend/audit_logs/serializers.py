from rest_framework import serializers
from .models import AuditLog


class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = [
            "id",
            "user",
            "agent",
            "request",
            "data_accessed",
            "tool",
            "action",
            "approval",
            "result",
            "timestamp",
        ]
        read_only_fields = ["id", "timestamp"]
