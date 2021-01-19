from django.urls import path

from .views import EmployeesAPIView, EmployeeDetailAPI

urlpatterns = [
    path('employees/', EmployeesAPIView.as_view(), name="employees-list"),
    path('employees/<int:pk>/', EmployeeDetailAPI.as_view(), name="employees-detail"),
]