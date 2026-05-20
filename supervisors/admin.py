from django.contrib import admin

from supervisors.models import Evaluation, SupervisorProfile


admin.site.register(SupervisorProfile)
admin.site.register(Evaluation)
