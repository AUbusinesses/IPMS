from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from students.models import StudentProfile
from users.models import UserProfile


@receiver(post_save, sender=UserProfile)
def create_student_profile(sender, instance, created, **kwargs):
    if instance.role == UserProfile.Role.STUDENT:
        StudentProfile.objects.get_or_create(user=instance.user)
