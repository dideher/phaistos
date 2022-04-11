from django.http.request import HttpRequest
from datetime import datetime

from bootstrap_modal_forms.generic import BSModalCreateView, BSModalUpdateView, BSModalReadView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponse, HttpResponseBadRequest
from django.http.request import HttpRequest
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils import timezone

from employees.models import Employee
from leaves.forms import LeaveForm, DeleteLeaveForm
from leaves.models import Leave
from phaistos.mixins import JsonableResponseMixin


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
    