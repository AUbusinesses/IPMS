from django.urls import path

from supervisors import views

urlpatterns = [
    path("dashboard/", views.supervisor_dashboard, name="supervisor_dashboard"),
    path("evaluations/new/", views.evaluation_create, name="evaluation_create"),
]
