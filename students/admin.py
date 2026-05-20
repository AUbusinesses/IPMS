from django.contrib import admin

from students.models import StudentProfile


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "student_id", "course", "gpa_wam", "preferred_location")
    search_fields = ("user__username", "user__email", "student_id", "course")
    filter_horizontal = ("skills",)
