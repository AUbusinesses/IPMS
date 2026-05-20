from django.contrib import admin

from internships.models import InternshipListing, Skill


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(InternshipListing)
class InternshipListingAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "employer",
        "domain",
        "location",
        "status",
        "application_deadline",
    )
    list_filter = ("status", "work_mode", "domain")
    search_fields = ("title", "description", "location")
    filter_horizontal = ("required_skills",)
