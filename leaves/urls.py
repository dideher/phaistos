from django.urls import path
from leaves.views import LeaveDeleteView, LeaveCreateView

app_name = 'leaves'

urlpatterns = [
    path('<int:pk>/delete', LeaveDeleteView.as_view(), name='leave-delete'),
    path('<int:employee_pk>/create', LeaveCreateView.as_view(), name='leave-create'),
]
