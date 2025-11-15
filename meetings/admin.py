from django.contrib import admin
from .models import Meeting, Room


@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_time', 'end_time', 'organizer')
    list_filter = ('start_time', 'organizer')
    search_fields = ('title', 'description')
    admin.site.register(Room)