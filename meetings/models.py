from django.db import models
from django.contrib.auth.models import User

class Room(models.Model):
    name = models.CharField(max_length=100, unique=True)
    capacity = models.PositiveIntegerField(default=20)
    def __str__(self):
        return self.name


class Meeting(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_meetings')
    participants = models.ManyToManyField(User, related_name='meetings')
    created_at = models.DateTimeField(auto_now_add=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True, blank=True)
    STATUS_CHOICES = [
            ('scheduled', '已安排'),
            ('cancelled', '已取消'),
        ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')

    important_participants = models.ManyToManyField(
        User,
        related_name='important_meetings',
        blank=True,
        help_text='重要参会人'
    )

    def __str__(self):
        return self.title

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'[{self.user}] {self.meeting.title}'

