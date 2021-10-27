from django import template
from django.db.models.query import QuerySet

from employees.models import Employee
from leaves.models import Leave

register = template.Library()

@register.inclusion_tag('employees/custom_tag_show_leaves.html', takes_context=True)
def show_leaves(context):
    employee: Employee = context.get('employee')
    if employee is not None:
        leaves: QuerySet[Leave] = Leave.objects.filter(employee_id=employee)
        return { 'leaves': leaves}
    else:
        return { 'leaves': None}
    