from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import FormMixin

from employees.forms import EmployeeSearchForm, SubstituteEmploymentAnnouncementSearchForm
from employees.models import Employee, SubstituteEmploymentAnnouncement
from main.models import SchoolYear
# from phaistos.commons.views import OurServerSideDatatableView
# class EmployeeListDatatableView(OurServerSideDatatableView):
#     # WONT USE IT FOR THE TIME
#
#     queryset = Employee.objects.filter(is_active=True)
#
#     columns = ['vat_number', 'registry_id', 'last_name', 'first_name', 'father_name', 'specialization__code',
#                'current_unit__title', 'employee_type', 'date_of_birth', 'uuid']


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

            last_name = form.cleaned_data['last_name']
            first_name = form.cleaned_data['first_name']
            vat_number = form.cleaned_data['vat_number']
            registry_id = form.cleaned_data['registration_id']

            if last_name and len(last_name) > 0:
                filters['last_name__contains'] = last_name.upper()

            if first_name and len(first_name) > 0:
                filters['first_name__contains'] = first_name.upper()

            if vat_number and len(vat_number) > 0:
                filters['vat_number__contains'] = vat_number

            if registry_id and len(registry_id) > 0:
                filters['registry_id__contains'] = registry_id

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

    def get_object(self, queryset=None):
        return Employee.objects.get(uuid=self.kwargs.get("uuid"))


class SubstituteEmploymentAnnouncementListView(LoginRequiredMixin, PermissionRequiredMixin, ListView ):

    model = SubstituteEmploymentAnnouncement
    context_object_name = 'announcements'
    paginator_per_page_count = 12
    form_class = SubstituteEmploymentAnnouncementSearchForm
    permission_required = ['employees.view_employee']
    template_name = 'employees/substitute/employment_announcement_list.html'

    def get_queryset(self):
        form = self.form_class(self.request.GET)

        if form.is_valid():
            filters = {}

            specialization = form.cleaned_data['specialization']
            school_year = form.cleaned_data['school_year']
            financing = form.cleaned_data['financing']
            employment_source = form.cleaned_data['employment_source']
            is_pending = form.cleaned_data['is_pending']

            if specialization:
                filters['specialization'] = specialization

            if school_year:
                filters['school_year'] = school_year

            if financing:
                filters['financing'] = financing

            if employment_source:
                filters['employment_source'] = employment_source

            return SubstituteEmploymentAnnouncement.objects.filter(**filters)
        else:
            # filtering form is not valid yet ?
            return SubstituteEmploymentAnnouncement.objects.all()


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class(initial=self.request.GET)
        return context