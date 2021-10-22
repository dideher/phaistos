from django.urls import path

from .views import EmployeesAPIView, EmployeeDetailAPI, SpecializationAPIView, SpecializationDetailAPI, EmployeeImportAPIView

urlpatterns = [
    path('employees/', EmployeesAPIView.as_view(), name="employees"),
    path('employees/<int:pk>/', EmployeeDetailAPI.as_view(), name="employee-detail"),
    path('employees_import/', EmployeeImportAPIView.as_view(), name='employees-import'),
    path('specializations/', SpecializationAPIView.as_view(), name="specializations"),
    path('specializations/<int:pk>/', SpecializationDetailAPI.as_view(), name="specialization-detail"),
]