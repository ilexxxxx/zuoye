from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Meeting
from .utils import notify_users

@receiver(post_save, sender=Meeting)
def meeting_saved(sender, instance, created, **kwargs):
    """后台新增或修改会议时自动发通知"""
    notify_users(instance, created=created)