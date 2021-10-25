from django.db.models.query import QuerySet
from employees.models import Employee, Specialization
from django.views.generic.list import ListView


class EmployeeListView(ListView):

    model = Employee
    paginate_by = 30  # if pagination is desired


