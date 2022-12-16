from django.urls import path
from employees.views import EmployeeListView
from leaves.views import (
    LeaveDeleteView,
    LeaveCreateView,
    LeaveDetailView,
    LeaveUpdateView,
    compute_leave_calendar_duration,
    LeaveSearchListView,
    EmployeeLeavesListView
)

app_name = 'leaves'

urlpatterns = [
    path('', EmployeeListView.as_view(), name="employee-list"),
    path('employee-leaves-list/<uuid:uuid>', EmployeeLeavesListView.as_view(), name='employee-leaves-list'),
    path('compute_leave_duration', compute_leave_calendar_duration, name='compute_leave_calendar_duration'),
    path('<int:pk>/view', LeaveDetailView.as_view(), name='leave-detail'),
    path('<int:pk>/delete', LeaveDeleteView.as_view(), name='leave-delete'),
    path('<int:pk>/update', LeaveUpdateView.as_view(), name='leave-update'),
    path('<uuid:employee_uuid>/create', LeaveCreateView.as_view(), name='leave-create'),
    path('search', LeaveSearchListView.as_view(), name='leave-search')
]
