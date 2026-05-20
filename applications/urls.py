from django.urls import path

from applications import views

urlpatterns = [
    path("", views.applications_list, name="applications_list"),
    path("apply/<int:internship_id>/", views.apply_to_internship, name="apply_to_internship"),
    path("<int:pk>/update/", views.update_application, name="update_application"),
    path("weekly-log/", views.weekly_log_create, name="weekly_log_create"),
    path("timesheet/", views.timesheet_create, name="timesheet_create"),
]
