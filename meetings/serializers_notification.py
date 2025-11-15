from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    meeting_title = serializers.CharField(source='meeting.title', read_only=True)

    class Meta:
        model = Notification
        fields = ('id', 'meeting_title', 'message', 'is_read', 'created_at')