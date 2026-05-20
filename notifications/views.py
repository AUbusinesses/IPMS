from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render


@login_required
def notifications_list(request):
    notifications = request.user.notifications.all()
    return render(request, "notifications/list.html", {"notifications": notifications})


@login_required
def mark_all_read(request):
    request.user.notifications.filter(is_read=False).update(is_read=True)
    return redirect("notifications_list")
