from django.urls import path
from employees.views import EmployeeListView, EmployeeDetailView, EmployeeLeavesListView

app_name = 'employees'

urlpatterns = [
    path('', EmployeeListView.as_view(), name="employee-list"),
    path('<int:pk>/', EmployeeDetailView.as_view(), name='employee-detail'),
    path('<int:pk>/leaves', EmployeeLeavesListView.as_view(), name='employee-leaves-list'),
]