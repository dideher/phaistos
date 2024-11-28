from ajax_datatable.views import AjaxDatatableView
from django.contrib.auth.models import Permission
from django.core.exceptions import PermissionDenied
from employees.models import Employee
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse, translate_url

@method_decorator(login_required, name='dispatch')
class BaseAjaxDatatableView(AjaxDatatableView):
    pass


class EmployeesAjaxDatatableView(BaseAjaxDatatableView):

    model = Employee
    title = 'Λίστα Εκπαιδευτικών'
    initial_order = [["last_name", "asc"], ["specialization", "asc"]]
    length_menu = [[10, 20, 50, 100, -1], [10, 20, 50, 100, 'Όλα']]
    search_values_separator = '+'

    column_defs = [
        #AjaxDatatableView.render_row_tools_column_def(),
        {'name': 'id', 'visible': False},
        {'name': 'registry_id', 'title': 'ΑΜ'},
        {'name': 'vat_number', 'title': 'ΑΦΜ'},
        {'name': 'last_name', 'title': 'Επώνυμο', 'searchable': True},
        {'name': 'first_name', 'title': 'Όνομα'},
        {'name': 'father_name', 'title': 'Όνομα Πατρός'},
        {'name': 'specialization', 'title': 'Ειδικότητα', 'foreign_field': "specialization__code", 'searchable': True},
        {'name': 'current_unit', 'title': 'Οργανική', 'foreign_field': "current_unit__title", 'searchable': True},
        {'name': 'employee_type', 'title': 'Τύπος', 'choices': True},
        {'name': 'date_of_birth', 'title': 'Ετ.Γεν.', 'searchable': False},
        {'name': 'goto_url', 'title': 'Goto URL', 'visible': False, 'placeholder': True, 'searchable': False, 'orderable': False},
    ]

    def get_initial_queryset(self, request=None):
        # We accept either GET or POST
        if not getattr(request, 'REQUEST', None):
            request.REQUEST = request.GET if request.method == 'GET' else request.POST

        queryset = super().get_initial_queryset(request=request)
        queryset = queryset.filter(is_active=True)

        return queryset

    def customize_row(self, row, obj: Employee):
        request = self.request
        if not getattr(request, 'REQUEST', None):
            request.REQUEST = request.GET if request.method == 'GET' else request.POST

        row['goto_url'] = reverse(request.REQUEST.get('goto_target'), args=(obj.uuid, ))
