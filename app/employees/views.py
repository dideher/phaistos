from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.utils import timezone
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from employees.forms import EmployeeSearchForm
from employees.models import Employee
from leaves.forms import LeaveSearchForm
from leaves.models import Leave
from phaistos.commons import (
    get_regular_leaves_for_employee_established_in_year,
    get_medical_leaves_for_employee_established_in_year,
    compute_leaves_real_duration
)


class EmployeeListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):

    model = Employee
    context_object_name = 'employees'
    paginator_per_page_count = 12
    form_class = EmployeeSearchForm
    permission_required = ['employees.view_employee']

    def get_queryset(self):
        form = self.form_class(self.request.GET)
        if form.is_valid():
            filters = {}
            if form.cleaned_data['last_name']:
                filters['last_name__contains'] = form.cleaned_data['last_name'].upper()

            if form.cleaned_data['first_name']:
                filters['first_name__contains'] = form.cleaned_data['first_name'].upper()

            if form.cleaned_data['enabled'] is None:
                filters['enabled'] = form.cleaned_data['enabled']

            if form.cleaned_data['employee_type'] not in [None, '']:
                filters['employee_type'] = form.cleaned_data['employee_type']

            return Employee.objects.filter(**filters).order_by('last_name', 'specialization')
        else:
            return Employee.objects.all().order_by('last_name', 'specialization')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class(initial=self.request.GET)
        paginator = Paginator(context['employees'], EmployeeListView.paginator_per_page_count)
        page = self.request.GET.get("page")

        try:
            objects = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            objects = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            objects = paginator.page(paginator.num_pages)
        
        context["employees_paginated"] = objects
        context["display_paginated_pages"] = paginator.num_pages > 1
        return context


class EmployeeDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = ['employees.view_employee']
    model = Employee


class EmployeeLeavesListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):

    model = Leave
    context_object_name = 'leaves'
    paginator_per_page_count = 12
    form_class = LeaveSearchForm
    template_name = 'employees/employee_leaves_list.html'
    permission_required = ['employees.view_employee', 'leaves.view_leave']

    def get_queryset(self):
        employee_id = self.kwargs['pk']
        if True:
            return Leave.objects.filter(employee=employee_id, is_deleted=False).order_by('-date_from', '-created_on')

        form = self.form_class(self.request.GET)

        if form.is_valid():
            filters = {}
            if form.cleaned_data['last_name']:
                filters['last_name__contains'] = form.cleaned_data['last_name'].upper()

            if form.cleaned_data['first_name']:
                filters['first_name__contains'] = form.cleaned_data['first_name'].upper()

            if form.cleaned_data['enabled'] is None:
                filters['enabled'] = form.cleaned_data['enabled']

            if form.cleaned_data['employee_type'] not in [None, '']:
                filters['employee_type'] = form.cleaned_data['employee_type']

            return Leave.objects.filter(**filters).order_by('last_name', 'specialization')
        else:
            return Leave.objects.all().order_by('last_name', 'specialization')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # add also the employee in the context
        employee: Employee = Employee.objects.get(id=self.kwargs['pk'])
        context['employee'] = employee
        
        context['form'] = self.form_class(initial=self.request.GET)
        paginator = Paginator(context['leaves'], EmployeeLeavesListView.paginator_per_page_count)
        page = self.request.GET.get("page")

        # compute some basic leave statistics
        today = timezone.now().date()

        context['regular_leaves_current_year'] = compute_leaves_real_duration(
            get_regular_leaves_for_employee_established_in_year(employee=employee, year=today.year)
        )
        context['regular_leaves_previous_year'] = compute_leaves_real_duration(
            get_regular_leaves_for_employee_established_in_year(employee=employee, year=today.year-1)
        )
        context['medical_leaves_current_year'] = compute_leaves_real_duration(
            get_medical_leaves_for_employee_established_in_year(employee=employee, year=today.year)
        )
        context['medical_leaves_last_5_years'] = compute_leaves_real_duration(
            get_medical_leaves_for_employee_established_in_year(employee=employee, year_from=today.year - 5,
                                                                year_until=today.year)
        )

        try:
            objects = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            objects = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            objects = paginator.page(paginator.num_pages)
        
        context["leaves_paginated"] = objects
        context["display_paginated_pages"] = paginator.num_pages > 1
        
        return context

