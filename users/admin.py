from django.contrib import admin

from users.models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "is_approved", "phone", "created_at")
    list_filter = ("role", "is_approved")
    search_fields = ("user__username", "user__email", "user__first_name", "user__last_name")
