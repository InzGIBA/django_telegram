from rest_framework import serializers

from .models import Message


class MessageSerializer(serializers.Serializer):
    body = serializers.CharField()

    def create(self, validated_data):
        return Message.objects.create(**validated_data)