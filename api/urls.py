from django.urls import path

from api.views import (
    EmployeesAPIView, 
    EmployeeDetailAPI, 
    SpecializationAPIView, 
    SpecializationDetailAPI, 
    EmployeeImportAPIView,
    LeaveTypesAPIView, 
    LeaveTypeDetailAPI, 
    LeaveImportAPIView
)

urlpatterns = [
    path('employees/', EmployeesAPIView.as_view(), name="employees"),
    path('employees/<int:pk>/', EmployeeDetailAPI.as_view(), name="employee-detail"),
    path('employees_import/', EmployeeImportAPIView.as_view(), name='employees-import'),
    path('specializations/', SpecializationAPIView.as_view(), name="specializations"),
    path('specializations/<int:pk>/', SpecializationDetailAPI.as_view(), name="specialization-detail"),
    path('leavetypes/', LeaveTypesAPIView.as_view(), name="leavetypes-list"),
    path('leavetypes/<int:pk>/', LeaveTypeDetailAPI.as_view(), name="leavetype-detail"),
    path('leaves_import/', LeaveImportAPIView.as_view(), name='leaves-import'),
]