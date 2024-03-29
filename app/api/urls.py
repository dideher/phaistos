from django.urls import path

from api.views import (
    EmployeeList,
    EmployeeDetailAPI, 
    SpecializationAPIView, 
    SpecializationDetailAPI, 
    EmployeeImportAPIView,
    LeaveTypesAPIView, 
    LeaveTypeDetailAPI, 
    LeaveImportAPIView,
    UnitImportAPIView,
    AthinaEmployeeImportAPIView,
    MySchoolEmployeeImportAPIView,
    MySchoolEmploymentImportAPIView,
    SchoolPrincipalList
)
from api.imports.myschool import SchoolPrincipalImportAPIView

urlpatterns = [
    path('employees/', EmployeeList.as_view(), name="employees-list"),
    path('employees/<int:pk>/', EmployeeDetailAPI.as_view(), name="employee-detail"),
    path('bulk_import/employees/', EmployeeImportAPIView.as_view(), name='employees-import'),
    path('bulk_import/units/', UnitImportAPIView.as_view(), name='units-import'),
    path('bulk_import/leaves/', LeaveImportAPIView.as_view(), name='leaves-import'),
    path('bulk_import/athina/employees/', AthinaEmployeeImportAPIView.as_view(), name='athina-employees-import'),
    path('bulk_import/myschool/employees/', MySchoolEmployeeImportAPIView.as_view(),
         name='myschool-employees-import'),
    path('bulk_import/myschool/employments/', MySchoolEmploymentImportAPIView.as_view(),
         name='myschool-employment-import'),
    path('bulk_import/myschool/schoolprincipals/', SchoolPrincipalImportAPIView.as_view(),
         name='myschool-schoolprincipals-import'),
    path('specializations/', SpecializationAPIView.as_view(), name="specializations"),
    path('specializations/<str:code>/', SpecializationDetailAPI.as_view(), name="specialization-detail"),
    path('leavetypes/', LeaveTypesAPIView.as_view(), name="leavetypes-list"),
    path('leavetypes/<int:pk>/', LeaveTypeDetailAPI.as_view(), name="leavetype-detail"),
    path('schoolprincipals/', SchoolPrincipalList.as_view(), name='school-principal-list')
]