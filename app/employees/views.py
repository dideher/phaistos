from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from employees.forms import EmployeeSearchForm
from employees.models import Employee


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

            # if form.cleaned_data['is_active'] is not None:
            #     filters['is_active'] = form.cleaned_data['is_active']
            #
            filters['is_active'] = True

            if form.cleaned_data['employee_type'] not in [None, '']:
                filters['employee_type'] = form.cleaned_data['employee_type']

            return Employee.objects.filter(**filters).order_by('last_name', 'specialization')
        else:
            return Employee.objects.all().order_by('last_name', 'specialization')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # put the goto_target variable to the context so the view can render correct views
        context['goto_target'] = self.kwargs.get('goto_target', 'employee-detail')
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


