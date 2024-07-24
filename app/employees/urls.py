from django.urls import path
from employees.views import EmployeeListView, EmployeeDetailView
from employees.ajax_datatable_views import EmployeesAjaxDatatableView
# from employees.views EmployeeListDatatableView


app_name = 'employees'

urlpatterns = [
    path('goto/<str:goto_target>', EmployeeListView.as_view(), name="employee-list"),
    path('ajax_datatable/employees/', EmployeesAjaxDatatableView.as_view(), name="ajax_datatable_employees"),
    # path('data/', EmployeeListDatatableView.as_view(), name='employee-list-data'),
    path('<uuid:uuid>', EmployeeDetailView.as_view(), name='employee-detail'),
]
