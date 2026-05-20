from django.db.models.signals import post_save
from django.dispatch import receiver

from employers.models import EmployerProfile
from users.models import UserProfile


@receiver(post_save, sender=UserProfile)
def create_employer_profile(sender, instance, created, **kwargs):
    if instance.role == UserProfile.Role.EMPLOYER:
        EmployerProfile.objects.get_or_create(
            user=instance.user,
            defaults={"company_name": f"{instance.user.username} Company"},
        )
