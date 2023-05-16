from django.contrib import admin
from .models import Employee, Specialization, Unit, EmployeeType, WorkExperience, WorkExperienceType, EmploymentType, \
    Employment


@admin.register(EmployeeType)
class EmployeeTypeAdmin(admin.ModelAdmin):
    list_display = ('title', 'legacy_type')
    search_fields = ('title',)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'registry_id', 'vat_number', 'last_name', 'first_name', 'father_name', 'employee_type')
    ordering = ('last_name', 'first_name', 'father_name', )
    search_fields = ('registry_id', 'vat_number', 'last_name', 'first_name', )


@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ('code', 'title', 'public_code', 'public_title', 'is_disabled')
    search_fields = ('code', 'title', 'public_code', 'public_title')
    ordering = ('code', )


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('ministry_code', 'title', 'unit_type', 'school_type', 'public_sector')
    search_fields = ('ministry_code', 'title')
    ordering = ('unit_type', 'title')


@admin.register(WorkExperienceType)
class WorkExperienceTypeAdmin(admin.ModelAdmin):
    list_display = ('code', 'description')
    search_fields = ('code', 'description')
    ordering = ('code', )


@admin.register(WorkExperience)
class WorkExperienceAdmin(admin.ModelAdmin):
    list_display = ('employee', 'work_experience_type', 'date_from', 'date_until', 'duration_total_in_days',
                    'duration_days', 'duration_months', 'duration_years')
    search_fields = ('employee', 'work_duration_total_in_days')
    ordering = ('employee', 'date_from')


@admin.register(Employment)
class EmploymentAdmin(admin.ModelAdmin):
    pass


@admin.register(EmploymentType)
class EmploymentTypeAdmin(admin.ModelAdmin):
    pass

