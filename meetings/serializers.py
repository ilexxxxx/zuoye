from rest_framework import serializers
from .models import Meeting, Room
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class MeetingSerializer(serializers.ModelSerializer):
    organizer = UserSerializer(read_only=True)
    participants = UserSerializer(read_only=True, many=True)
    room_name = serializers.CharField(source='room.name', read_only=True, allow_null=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    participant_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False
    )
    important_participant_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    important_participants = UserSerializer(read_only=True, many=True)

    class Meta:
        model = Meeting
        fields = (
            'id', 'title', 'description', 'start_time', 'end_time',
            'organizer', 'participants', 'created_at', 'participant_ids','room',
            'room_name', 'status', 'status_display', 'important_participant_ids', 'important_participants'
        )

    def validate(self, attrs):
        start = attrs.get('start_time')
        end = attrs.get('end_time')
        if start and end and start >= end:
            raise serializers.ValidationError("结束时间必须晚于开始时间！")

        user = self.context['request'].user
        conflicts = Meeting.objects.filter(
            organizer=user,
            start_time__lt=end,
            end_time__gt=start
        )
        if self.instance:
            conflicts = conflicts.exclude(pk=self.instance.pk)
        if conflicts.exists():
            raise serializers.ValidationError("与现有会议时间冲突！")
        return attrs

    def create(self, validated_data):
        important_participant_ids = validated_data.pop('important_participant_ids', [])
        validated_data.pop('participant_ids', None)
        meeting = super().create(validated_data)
        if important_participant_ids:
            meeting.important_participants.set(
                User.objects.filter(id__in=important_participant_ids)
            )
        return meeting

    def update(self, instance, validated_data):
        important_participant_ids = validated_data.pop('important_participant_ids', None)
        validated_data.pop('participant_ids', None)

        instance = super().update(instance, validated_data)

        if important_participant_ids is not None:
            instance.important_participants.set(
                User.objects.filter(id__in=important_participant_ids)
            )
        return instance

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'
