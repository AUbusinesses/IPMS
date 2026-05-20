from django.db.models.signals import post_save
from django.dispatch import receiver

from supervisors.models import SupervisorProfile
from users.models import UserProfile


@receiver(post_save, sender=UserProfile)
def create_supervisor_profile(sender, instance, created, **kwargs):
    if instance.role == UserProfile.Role.SUPERVISOR:
        SupervisorProfile.objects.get_or_create(user=instance.user)
