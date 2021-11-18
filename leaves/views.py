from django.core import paginator
from django.utils import timezone
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import DeletionMixin, CreateView

from phaistos.mixins import JsonableResponseMixin

from leaves.models import Leave
from leaves.forms import LeaveForm
from employees.models import Employee

class BaseDeleteView(SingleObjectMixin, DeletionMixin, View):

    def setup(self, request, *args, **kwargs):

        super().setup(request, *args, **kwargs)
        
        if request.POST is not None:
            self.success_url = request.POST['success_url']

    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL.
        """
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.is_deleted = True
        self.object.deleted_on = timezone.now()
        self.object.deleted_comment = request.POST.get('delete_comment_text')
        self.object.save()
        return HttpResponseRedirect(success_url)

class LeaveDeleteView(LoginRequiredMixin, BaseDeleteView):

    model = Leave

    
class LeaveCreateView(LoginRequiredMixin, JsonableResponseMixin, CreateView):

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
        self.object: Leave = form.save(commit=False)
        self.object.employee = self.employee
        self.object.minoas_id
        return super().form_valid(form)


    def get_success_url(self):
           return reverse("employees:employee-leaves-list", kwargs={"pk": self.employee.id})



    
    