from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import UserProfile


@receiver(post_save, sender=get_user_model())
def ensure_admin_profile(sender, instance, created, **kwargs):
    if not created or hasattr(instance, "userprofile"):
        return
    role = UserProfile.Role.ADMIN if instance.is_superuser else UserProfile.Role.STUDENT
    UserProfile.objects.create(
        user=instance,
        role=role,
        is_approved=instance.is_superuser,
    )
