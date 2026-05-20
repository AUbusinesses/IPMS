from django.urls import path

from employers import views

urlpatterns = [
    path("dashboard/", views.employer_dashboard, name="employer_dashboard"),
    path("profile/", views.employer_profile, name="employer_profile"),
]
