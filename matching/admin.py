from django.contrib import admin

from matching.models import MatchRecord


@admin.register(MatchRecord)
class MatchRecordAdmin(admin.ModelAdmin):
    list_display = ("student", "internship", "score", "created_at")
    list_filter = ("score",)
    search_fields = ("student__user__username", "internship__title")
