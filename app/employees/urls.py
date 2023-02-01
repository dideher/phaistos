from django.urls import path
from employees.views import EmployeeListView, EmployeeDetailView
# from employees.views EmployeeListDatatableView

app_name = 'employees'

urlpatterns = [
    path('goto/<str:goto_target>', EmployeeListView.as_view(), name="employee-list"),
    # path('data/', EmployeeListDatatableView.as_view(), name='employee-list-data'),
    path('<uuid:uuid>', EmployeeDetailView.as_view(), name='employee-detail'),
]
