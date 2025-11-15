from .models import Meeting, Room
from .serializers import MeetingSerializer, RoomSerializer, UserSerializer
from .utils import notify_users
from django.contrib.auth.models import User
from .models import Notification
from .serializers_notification import NotificationSerializer
from rest_framework.decorators import action
from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Meeting

@api_view(['GET'])
def current_user(request):
    return Response(UserSerializer(request.user).data)

class MeetingViewSet(viewsets.ModelViewSet):
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer

    def perform_create(self, serializer):
        meeting = serializer.save(organizer=self.request.user)
        participant_ids = self.request.data.get('participant_ids', [])
        meeting.participants.set(User.objects.filter(id__in=participant_ids))
        notify_users(meeting, created=True)

    def perform_update(self, serializer):
        meeting = serializer.save()
        participant_ids = self.request.data.get('participant_ids', [])
        meeting.participants.set(User.objects.filter(id__in=participant_ids))
        notify_users(meeting, created=False)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """取消会议"""
        meeting = self.get_object()
        meeting.status = 'cancelled' if meeting.status != 'cancelled' else 'scheduled'
        meeting.save()
        return Response({'message': '会议状态已更新'})

    @action(detail=True, methods=['post'])
    def delete_meeting(self, request, pk=None):
        """删除会议"""
        meeting = self.get_object()
        if meeting.status == 'cancelled':
            meeting.delete()
            return Response({'message': '会议已删除'})
        else:
            return Response({'error': '只有已取消的会议可以被删除'}, status=status.HTTP_400_BAD_REQUEST)

class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return self.request.user.notifications.all().order_by('-created_at')

    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        """当前用户全部标为已读"""
        updated = request.user.notifications.filter(is_read=False).update(is_read=True)
        return Response({'message': f'已标记 {updated} 条为已读'})

# 注册视图
@api_view(['POST'])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if User.objects.filter(username=username).exists():
        return Response({'error': '用户名已存在'}, status=status.HTTP_400_BAD_REQUEST)
    user = User.objects.create_user(username=username, password=password)
    return Response({'id': user.id, 'username': user.username}, status=status.HTTP_201_CREATED)

class RoomViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

@api_view(['POST'])
def check_conflict(request):
# 冲突检测
    room_id   = request.data.get('room')
    start     = request.data.get('start_time')
    end       = request.data.get('end_time')
    pid_list  = request.data.get('participant_ids', [])

    conflicts = []

    # 1. 会议室冲突
    room_qs = Meeting.objects.filter(
        room_id=room_id,
        start_time__lt=end,
        end_time__gt=start
    )
    if room_qs.exists():
        conflicts.append(f"会议室 {room_qs.first().room.name} 时段已被占用！")

    # 2. 人员冲突
    people_qs = Meeting.objects.filter(
        participants__in=pid_list,
        start_time__lt=end,
        end_time__gt=start
    ).distinct()
    if people_qs.exists():
        conflicts.append(f"参会人员时间冲突：{', '.join(people_qs.values_list('title', flat=True))}")

    return Response({'conflicts': conflicts, 'ok': len(conflicts) == 0})

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

