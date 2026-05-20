from django.contrib import admin

from employers.models import EmployerProfile


@admin.register(EmployerProfile)
class EmployerProfileAdmin(admin.ModelAdmin):
    list_display = ("company_name", "user", "industry", "location", "is_verified")
    list_filter = ("is_verified", "industry")
    search_fields = ("company_name", "user__email", "location")
