from django.core import paginator
from django.http.request import HttpRequest
from django.utils import timezone
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import DeletionMixin, CreateView
from datetime import datetime, timedelta
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalUpdateView, BSModalReadView

from phaistos.mixins import JsonableResponseMixin

from leaves.models import Leave
from leaves.forms import LeaveForm, DeleteLeaveForm
from employees.models import Employee


class BaseDeleteView(BSModalUpdateView):

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.is_deleted = True
        instance.deleted_on = timezone.now()
        return super(BaseDeleteView, self).form_valid(form)


class LeaveDeleteView(LoginRequiredMixin, BaseDeleteView):
    template_name = 'leaves/delete_leave.html'
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


class LeaveDetailView(BSModalReadView):
    model = Leave


class LeaveCreateView(LoginRequiredMixin, JsonableResponseMixin, BSModalCreateView):

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


class LeaveUpdateView(LoginRequiredMixin, JsonableResponseMixin, BSModalUpdateView):
    model = Leave
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
    