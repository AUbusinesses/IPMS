from django.contrib import admin

from applications.models import InternshipApplication, Timesheet, WeeklyLog


@admin.register(InternshipApplication)
class InternshipApplicationAdmin(admin.ModelAdmin):
    list_display = ("student", "internship", "status", "applied_at")
    list_filter = ("status",)
    search_fields = ("student__user__username", "internship__title")


admin.site.register(WeeklyLog)
admin.site.register(Timesheet)
