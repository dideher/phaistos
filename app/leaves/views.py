from datetime import datetime
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalUpdateView, BSModalReadView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponse, HttpResponseBadRequest
from django.http.request import HttpRequest
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils import timezone
from phaistos.commons.export import ExportableListView

from employees.models import Employee
from leaves.forms import LeaveForm, DeleteLeaveForm, LeaveSearchForm
from leaves.models import Leave
from phaistos.commons.mixins import JsonableResponseMixin


class BaseDeleteView(BSModalUpdateView):

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.is_deleted = True
        instance.deleted_on = timezone.now()
        return super(BaseDeleteView, self).form_valid(form)


class LeaveDeleteView(LoginRequiredMixin, PermissionRequiredMixin, BaseDeleteView):
    template_name = 'leaves/delete_leave.html'
    permission_required = ['leaves.delete_leave']
    form_class = DeleteLeaveForm
    model = Leave
    success_message = 'Η διαγραφή της άδειας έγινε με επιτυχεία!'

    def get_success_url(self):
        return reverse("employees:employee-leaves-list", kwargs={"pk": self.object.employee.id})


def compute_leave_calendar_duration(request: HttpRequest):
    if request.method == 'POST':
        
        date_from = request.POST.get('date_from')
        date_until = request.POST.get('date_until')
        try:
            date_from_date = datetime.strptime(date_from, '%d/%m/%Y')
            date_until_date = datetime.strptime(date_until, '%d/%m/%Y')
            return HttpResponse(1+(date_until_date.date() - date_from_date.date()).days)
        except ValueError:
            return HttpResponseBadRequest()

    else:
        return HttpResponse("")


class LeaveDetailView(LoginRequiredMixin, PermissionRequiredMixin, BSModalReadView):
    permission_required = ['leaves.view_leave']
    model = Leave


class LeaveCreateView(LoginRequiredMixin, PermissionRequiredMixin, JsonableResponseMixin, BSModalCreateView):
    permission_required = ['leaves.add_leave']
    model = Leave
    form_class = LeaveForm

    def dispatch(self, request, *args, **kwargs):
        """
        Overridden so we can make sure the `Ipsum` instance exists
        before going any further.
        """
        self.employee: Employee = get_object_or_404(Employee, pk=kwargs['employee_pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(LeaveCreateView, self).get_form_kwargs()
        kwargs['employee_id'] = self.employee.id
        
        return kwargs

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        leave: Leave = form.instance
        leave.employee = self.employee
        leave.number_of_days = (leave.date_until - leave.date_from).days + 1
        leave.created_on = timezone.now()
        leave.minoas_id = None

        messages.success(self.request, f'Η άδεια καταχωρήθηκε επιτυχώς')

        return super().form_valid(form)

    def get_success_url(self):
        return reverse("employees:employee-leaves-list", kwargs={"pk": self.employee.id})


class LeaveUpdateView(LoginRequiredMixin, PermissionRequiredMixin, JsonableResponseMixin, BSModalUpdateView):
    model = Leave
    permission_required = ['leaves.change_leave']
    template_name = 'leaves/update_leave.html'
    form_class = LeaveForm

    def get_object(self, queryset=None):
        return super(LeaveUpdateView, self).get_object(queryset=queryset)

    def form_valid(self, form):
        leave: Leave = form.instance
        leave.updated_on = timezone.now()
        messages.success(self.request, f'Η άδεια τροποποιήθηκε επιτυχώς')

        return super().form_valid(form)

    def get_success_url(self):
        return reverse("employees:employee-leaves-list", kwargs={"pk": self.object.employee.id})

    def get_form_kwargs(self):
        kwargs = super(LeaveUpdateView, self).get_form_kwargs()
        kwargs['employee_id'] = self.object.employee.id

        return kwargs


class LeaveSearchListView(LoginRequiredMixin, PermissionRequiredMixin, ExportableListView):
    model = Leave
    context_object_name = 'leaves'
    paginator_per_page_count = 12
    form_class = LeaveSearchForm
    template_name = 'leaves/search_leave.html'
    permission_required = ['leaves.search_leave']
    export_header = [
        'ID',
        'Επώνυμο',
        'Όνομα',
        'Πατρώνυμο',
        'Τύπος',
        'Ειδικότητα',
        'Κωδ.Άδ.',
        'Τύπος Άδειας',
        'Ημέρες',
        'Έναρξη',
        'Λήξη',
        'Ημ/νια Καταχώρισης'
        'Σχόλια',
    ]
    export_fields = [
        'id',
        'employee.last_name',
        'employee.first_name',
        'employee.father_name',
        'employee.get_employee_type_display',
        'employee.specialization.code',
        'leave_type.legacy_code',
        'leave_type.description',
        'effective_number_of_days',
        'date_from',
        'date_until',
        'created_on',
        'comment'

    ]
    export_filename = 'leaves-report'

    def get_queryset(self):

        qs = Leave.objects.filter(is_deleted=False)

        form = self.form_class(self.request.GET)
        if form.is_valid():
            filters = {}

            leave_types = form.cleaned_data['leave_type']
            effective_days_operator = form.cleaned_data['effective_days_operator']

            date_from = form.cleaned_data['date_from']
            date_from_operator = form.cleaned_data['date_from_operator']

            date_until = form.cleaned_data['date_until']
            date_until_operator = form.cleaned_data['date_until_operator']

            employee_type = form.cleaned_data['employee_type']

            try:
                effective_days = int(form.cleaned_data['effective_days'])
            except TypeError:
                effective_days = None

            if leave_types is not None and len(leave_types) > 0:
                filters['leave_type__in'] = leave_types

            if employee_type is not None and len(employee_type) > 0:
                print(employee_type)
                filters['employee__employee_type'] = employee_type

            if effective_days is not None:

                if effective_days_operator == LeaveSearchForm.EQUAL_TO:
                    filters['effective_number_of_days'] = effective_days
                elif effective_days_operator == LeaveSearchForm.GREATER_THAN_OR_EQUAL:
                    filters['effective_number_of_days__gte'] = effective_days
                elif effective_days_operator == LeaveSearchForm.LESS_THAN_OR_EQUAL:
                    filters['effective_number_of_days__lte'] = effective_days

            if date_from is not None:
                if date_from_operator == LeaveSearchForm.EQUAL_TO:
                    filters['date_from'] = date_from
                elif date_from_operator == LeaveSearchForm.GREATER_THAN_OR_EQUAL:
                    filters['date_from__gte'] = date_from
                elif date_from_operator == LeaveSearchForm.LESS_THAN_OR_EQUAL:
                    filters['date_from__lte'] = date_from

            if date_until is not None:
                print(date_until)
                print(date_until_operator)
                if date_until_operator == LeaveSearchForm.EQUAL_TO:
                    filters['date_until'] = date_until
                elif date_until_operator == LeaveSearchForm.GREATER_THAN_OR_EQUAL:
                    filters['date_until__gte'] = date_until
                elif date_until_operator == LeaveSearchForm.LESS_THAN_OR_EQUAL:
                    filters['date_until__lte'] = date_until

            qs = qs.filter(**filters)

        return qs.order_by('-date_from', '-created_on')

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['form'] = self.form_class(initial=self.request.GET)
        paginator = Paginator(context['leaves'], LeaveSearchListView.paginator_per_page_count)
        page = self.request.GET.get("page")

        # compute some basic leave statistics
        today = timezone.now().date()

        # context['regular_leaves_current_year'] = compute_leaves_real_duration(
        #     get_regular_leaves_for_employee_established_in_year(employee=employee, year=today.year)
        # )
        # context['regular_leaves_previous_year'] = compute_leaves_real_duration(
        #     get_regular_leaves_for_employee_established_in_year(employee=employee, year=today.year - 1)
        # )
        # context['medical_leaves_current_year'] = compute_leaves_real_duration(
        #     get_medical_leaves_for_employee_established_in_year(employee=employee, year=today.year)
        # )
        # context['medical_leaves_last_5_years'] = compute_leaves_real_duration(
        #     get_medical_leaves_for_employee_established_in_year(employee=employee, year_from=today.year - 5,
        #                                                         year_until=today.year)
        # )

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

