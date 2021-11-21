from django.urls import path
from leaves.views import LeaveDeleteView, LeaveCreateView, compute_leave_calendar_duration

app_name = 'leaves'

urlpatterns = [
    path('compute_leave_duration', compute_leave_calendar_duration, name='compute_leave_calendar_duration'),
    path('<int:pk>/delete', LeaveDeleteView.as_view(), name='leave-delete'),
    path('<int:employee_pk>/create', LeaveCreateView.as_view(), name='leave-create'),
]
