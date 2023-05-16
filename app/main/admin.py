from django.contrib import admin
from .models import SchoolYear


@admin.register(SchoolYear)
class SchoolYearAdmin(admin.ModelAdmin):
    pass