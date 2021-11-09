from django.urls import path
from leaves.views import LeaveDeleteView

app_name = 'leaves'

urlpatterns = [
    path('<int:pk>/delete', LeaveDeleteView.as_view(), name='leave-delete'),
]
