from django.urls import path
from employees.views import EmployeeListView, EmployeeDetailView

app_name = 'employees'

urlpatterns = [
    path('goto/<str:goto_target>', EmployeeListView.as_view(), name="employee-list"),
    path('<uuid:uuid>', EmployeeDetailView.as_view(), name='employee-detail'),
]