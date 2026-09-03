from rest_framework import serializers

from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    """
    Serializer for notification API responses.
    """

    username = serializers.CharField(
        source="user.username",
        read_only=True,
    )

    email = serializers.EmailField(
        source="user.email",
        read_only=True,
    )

    class Meta:
        model = Notification

        fields = [
            "id",
            "user",
            "username",
            "email",
            "notification_type",
            "title",
            "message",
            "priority",
            "channel",
            "is_read",
            "related_id",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "username",
            "email",
            "created_at",
        ]
