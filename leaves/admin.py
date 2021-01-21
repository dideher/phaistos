from django.contrib import admin

from leaves.models import LeaveType, Leave

# Register your models here.
admin.site.register(LeaveType)
admin.site.register(Leave)
