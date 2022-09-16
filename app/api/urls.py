from django.urls import path

from api.views import (
    EmployeeListAPIView,
    EmployeeDetailAPI, 
    SpecializationAPIView, 
    SpecializationDetailAPI, 
    EmployeeImportAPIView,
    LeaveTypesAPIView, 
    LeaveTypeDetailAPI, 
    LeaveImportAPIView,
    UnitImportAPIView,
    AthinaEmployeeImportAPIView
)

urlpatterns = [
    path('employees/', EmployeeListAPIView.as_view(), name="employees-list"),
    path('employees/<int:pk>/', EmployeeDetailAPI.as_view(), name="employee-detail"),
    path('bulk_import/employees/', EmployeeImportAPIView.as_view(), name='employees-import'),
    path('bulk_import/units/', UnitImportAPIView.as_view(), name='units-import'),
    path('bulk_import/leaves/', LeaveImportAPIView.as_view(), name='leaves-import'),
    path('bulk_import/athina/employees/', AthinaEmployeeImportAPIView.as_view(), name='athina-employees-import'),
    path('specializations/', SpecializationAPIView.as_view(), name="specializations"),
    path('specializations/<str:code>/', SpecializationDetailAPI.as_view(), name="specialization-detail"),
    path('leavetypes/', LeaveTypesAPIView.as_view(), name="leavetypes-list"),
    path('leavetypes/<int:pk>/', LeaveTypeDetailAPI.as_view(), name="leavetype-detail"),
]