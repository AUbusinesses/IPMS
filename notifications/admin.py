from django.contrib import admin

from notifications.models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("user", "title", "is_read", "email_sent", "created_at")
    list_filter = ("is_read", "email_sent")
    search_fields = ("title", "message", "user__username")
