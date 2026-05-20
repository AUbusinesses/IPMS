from django.urls import path

from matching import views

urlpatterns = [path("recommendations/", views.recommendations, name="recommendations")]
