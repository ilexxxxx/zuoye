from .models import Notification

def notify_users(meeting, created=False, cancelled=False):
    """通知用户有关会议的信息"""
    message = ""

    if cancelled:
        message = f"您参与的会议 '{meeting.title}' 已被取消。"
    elif created:
        message = f"您有一个新会议邀请: {meeting.title}"
    else:
        message = f"会议 '{meeting.title}' 信息已更新。"

    # 为重要参会人创建通知
    important_users = meeting.important_participants.all()
    regular_participants = meeting.participants.exclude(
        id__in=important_users.values_list('id', flat=True)
    )

    for user in important_users:
        Notification.objects.create(
            user=user,
            meeting=meeting,
            message="【重要】" + message
        )

    for user in regular_participants:
        Notification.objects.create(
            user=user,
            meeting=meeting,
            message=message
        )