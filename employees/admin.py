from django.contrib import admin
from .models import Employee, Specialization, Unit


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'father_name', 'employee_type')
    ordering = ('last_name', 'first_name', 'father_name', )
    search_fields = ('last_name', 'first_name', )


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
