from rest_framework import serializers

from django.contrib.auth.models import User

from .models import UserProfile, Conversation, ChatMessage


class UserRoleSerializer(serializers.ModelSerializer):

    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)

    name = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = [
            "id",
            "username",
            "name",
            "email",
            "role",
        ]

    def get_name(self, obj):

        full_name = obj.user.get_full_name().strip()

        if full_name:
            return full_name

        return obj.user.username


class ChatMessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChatMessage
        fields = [
            "id",
            "sender",
            "content",
            "created_at",
        ]


class ConversationSerializer(serializers.ModelSerializer):

    messages = ChatMessageSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Conversation
        fields = [
            "id",
            "title",
            "created_at",
            "updated_at",
            "messages",
        ]
