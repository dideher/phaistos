from django.urls import path

from leaves.views import LeaveTypesAPIView, LeaveTypeDetailAPI

urlpatterns = [
    path('leavetypes/', LeaveTypesAPIView.as_view(), name="leavetypes-list"),
    path('leavetypes/<int:pk>/', LeaveTypeDetailAPI.as_view(), name="leavetype-detail"),
]