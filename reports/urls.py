from django.urls import path

from reports import views

urlpatterns = [
    path("", views.reports_dashboard, name="reports_dashboard"),
    path("employers/<int:pk>/approve/", views.approve_employer, name="approve_employer"),
    path("internships/<int:pk>/approve/", views.approve_internship, name="approve_internship"),
    path("export/csv/", views.export_csv, name="export_csv"),
    path("export/pdf/", views.export_pdf, name="export_pdf"),
]
