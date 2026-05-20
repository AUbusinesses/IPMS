from django.urls import path

from internships import views

urlpatterns = [
    path("", views.internship_list, name="internship_list"),
    path("create/", views.internship_create, name="internship_create"),
    path("<int:pk>/", views.internship_detail, name="internship_detail"),
    path("<int:pk>/edit/", views.internship_edit, name="internship_edit"),
]
