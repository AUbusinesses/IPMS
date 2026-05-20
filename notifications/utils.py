from django.core.mail import send_mail
from django.conf import settings

from notifications.models import Notification


def create_notification(user, title, message, send_email=False):
    notification = Notification.objects.create(user=user, title=title, message=message)
    if send_email and user.email:
        send_mail(title, message, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=True)
        notification.email_sent = True
        notification.save(update_fields=["email_sent"])
    return notification
