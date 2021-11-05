from django.core import paginator
from django.db.models.query import QuerySet
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib import messages
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from employees.models import Employee, Specialization
from employees.forms import EmployeeSearchForm
class EmployeeListView(LoginRequiredMixin, ListView):

    model = Employee
    context_object_name = 'employees'
    paginator_per_page_count = 20
    form_class = EmployeeSearchForm

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
        
        return context


class EmployeeDetailView(DetailView):

    model = Employee