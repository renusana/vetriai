from django.contrib import admin
from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "agent",
        "tool",
        "action",
        "approval",
        "timestamp",
    )

    list_filter = (
        "agent",
        "tool",
        "approval",
        "timestamp",
    )

    search_fields = (
        "user",
        "agent",
        "request",
        "data_accessed",
        "tool",
        "action",
        "result",
    )

    readonly_fields = ("timestamp",)
