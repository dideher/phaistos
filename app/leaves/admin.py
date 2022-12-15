from django.contrib import admin
from leaves.models import LeaveType, Leave

# Register your models here.


@admin.register(LeaveType)
class LeaveTypeAdmin(admin.ModelAdmin):

    list_display = ('id', 'legacy_code', 'description', 'basic_type', 'suitable_for_employee_type')
    search_fields = ('description', 'legacy_code')
    ordering = ('legacy_code', )


@admin.register(Leave)
class LeaveAdmin(admin.ModelAdmin):
    list_display = ('id', 'employee', 'date_from', 'date_until', 'number_of_days', 'effective_number_of_days', 'leave_type', 'comment', 'is_deleted')
    search_fields = ('employee__last_name', )
    ordering = ('date_from', 'leave_type', )
