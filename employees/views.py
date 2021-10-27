from django.db.models.query import QuerySet
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from employees.models import Employee, Specialization

class EmployeeListView(LoginRequiredMixin, ListView):

    model = Employee
    paginate_by = 30  # if pagination is desired


class EmployeeDetailView(DetailView):

    model = Employee