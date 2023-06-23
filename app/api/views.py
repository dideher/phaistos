import json
import logging

from django.db.models.query import QuerySet
from django.utils.timezone import now
from django.db import transaction

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status

from rest_framework.generics import get_object_or_404, CreateAPIView, ListCreateAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.exceptions import ValidationError
from api.serializers import (
    EmployeeSerializer,
    EmploymentSerializer,
    SpecializationSerializer, 
    EmployeeImportSerializer,
    LeaveImportSerializer,
    LeaveSerializer,
    LeaveTypeSerializer,
    UnitImportSerializer,
    UnitSerializer,
    AthinaEmployeeImportSerializer,
    MySchoolEmployeeImportSerializer,
    MySchoolEmploymentImportSerializer,
    SubstituteEmploymentAnnouncementImportSerializer,

)
from api.core.pagination import StandardResultsSetPagination
from api.cache import get_cached_employee_type, get_cached_employee_specialization, get_cached_unit, get_cached_employment_type
from employees.models import (
    Employee, 
    Specialization,
    Unit,
    UnitType,
    EmployeeType,
    LegacyEmployeeType,
    WorkExperience,
    WorkExperienceType,
    Employment,
    EmploymentType,
    EmploymentFinancialSource,
    SubstituteEmploymentAnnouncement,
    SubstituteEmploymentSource
)
from leaves.models import (
    Leave,
    LeaveType,
)
from main.models import SchoolYear


class EmployeeList(ListCreateAPIView):

    serializer_class = EmployeeSerializer
    permission_classes = [IsAdminUser, ]

    def get_queryset(self):
        return Employee.objects.filter(is_active=True)

    def list(self, request, *args, **kwargs):

        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class UnitImportAPIView(APIView):

    def insert_or_update_general_unit(self, serializer: UnitImportSerializer) -> Response:

        validated_data = serializer.validated_data

        try:
            general_unit: Unit = Unit.objects.get(minoas_id=validated_data.get('minoas_id'))
        except Unit.DoesNotExist:
            general_unit = None

        if general_unit is None:

            general_unit = Unit.objects.create(
                minoas_id=validated_data.get('minoas_id'),
                title=validated_data.get('title'),
                public_sector=validated_data.get('public_sector'),
                school_type=None,
                unit_type=UnitType.OTHER,
            )

            school_serializer = UnitSerializer(general_unit)
            return Response(school_serializer.data, status=status.HTTP_201_CREATED)

        else:
            general_unit.title = validated_data.get('title')
            general_unit.public_sector = validated_data.get('public_sector')

            general_unit.save()
            school_serializer = UnitSerializer(general_unit)
            return Response(school_serializer.data, status=status.HTTP_200_OK)

    def insert_or_update_school(self, serializer: UnitImportSerializer) -> Response:

        validated_data = serializer.validated_data

        try:
            school: Unit = Unit.objects.get(minoas_id=validated_data.get('minoas_id'))
        except Unit.DoesNotExist:
            school = None

        if school is None:

            school = Unit.objects.create(
                minoas_id=validated_data.get('minoas_id'),
                title=validated_data.get('title'),
                school_type=validated_data.get('school_type'),
                ministry_code=validated_data.get('ministry_code'),
                points=validated_data.get('points'),
                public_sector=validated_data.get('public_sector'),
                unit_type=UnitType.SCHOOL,
            )

            school_serializer = UnitSerializer(school)
            return Response(school_serializer.data, status=status.HTTP_201_CREATED)

        else:
            school.title = validated_data.get('title')
            school.school_type = validated_data.get('school_type')
            school.ministry_code = validated_data.get('ministry_code')
            school.points = validated_data.get('points')
            school.public_sector = validated_data.get('public_sector')

            school.save()
            school_serializer = UnitSerializer(school)

            return Response(school_serializer.data, status=status.HTTP_200_OK)

    def post(self, request):

        serializer = UnitImportSerializer(data=request.data)

        if serializer.is_valid():
            validated_data = serializer.validated_data
            if validated_data.get('is_school', False) is True:
                return self.insert_or_update_school(serializer)
            elif validated_data.get('is_general_unit', False) is True:
                return self.insert_or_update_general_unit(serializer)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployeeImportAPIView(APIView):

    def post(self, request):
        
        serializer = EmployeeImportSerializer(data=request.data)
        
        if serializer.is_valid():
            validated_data = serializer.validated_data
            
            try:
                specialization: Specialization = Specialization.objects.get(code=validated_data.get('specialization_code'))
            except Specialization.DoesNotExist:
                specialization = None

            try:
                employee: Employee = Employee.objects.get(minoas_id=validated_data.get('minoas_id'))
            except Employee.DoesNotExist:
                employee = None

            current_unit_id = validated_data.get('current_unit_id')
            if current_unit_id is not None:
                try:
                    current_unit = Unit.objects.get(minoas_id=current_unit_id)
                except Unit.DoesNotExist:
                    current_unit = None
            else:
                current_unit = None

            if employee is None:

                employee = Employee.objects.create(
                    minoas_id=validated_data.get('minoas_id'),
                    big_family=validated_data.get('big_family'),
                    comment=validated_data.get('comment'),
                    date_of_birth=validated_data.get('date_of_birth'),
                    email=validated_data.get('email'),
                    father_name=validated_data.get('father_name'),
                    father_surname=validated_data.get('father_surname'),
                    first_name=validated_data.get('first_name'),
                    last_name=validated_data.get('last_name'),
                    id_number=validated_data.get('id_number'),
                    id_number_authority = validated_data.get('id_number_authority'),
                    is_man=validated_data.get('is_man'),
                    mother_name=validated_data.get('mother_name'),
                    mother_surname=validated_data.get('mother_surname'),
                    vat_number=validated_data.get('vat_number'),
                    employee_type=validated_data.get('employee_type'),
                    marital_status=validated_data.get('marital_status'),
                    specialization=specialization,
                    registry_id=validated_data.get('registry_id'),
                    current_unit=current_unit,
                    is_active=validated_data.get('is_active')
                )

                employee_serializer = EmployeeSerializer(employee)
                return Response(employee_serializer.data, status=status.HTTP_201_CREATED)

            else:
                employee.big_family = validated_data.get('big_family')
                employee.comment = validated_data.get('comment')
                employee.date_of_birth =validated_data.get('date_of_birth')
                employee.email = validated_data.get('email')
                employee.father_name = validated_data.get('father_name')
                employee.father_surname = validated_data.get('father_surname')
                employee.first_name = validated_data.get('first_name')
                employee.last_name = validated_data.get('last_name')
                employee.id_number = validated_data.get('id_number')
                employee.id_number_authority = validated_data.get('id_number_authority')
                employee.is_man = validated_data.get('is_man')
                employee.mother_name = validated_data.get('mother_name')
                employee.mother_surname = validated_data.get('mother_surname')
                employee.vat_number = validated_data.get('vat_number')
                employee.employee_type = validated_data.get('employee_type')
                employee.marital_status = validated_data.get('marital_status')
                employee.specialization = specialization
                employee.registry_id = validated_data.get('registry_id')
                employee.current_unit = current_unit
                employee.is_active = validated_data.get('is_active')

                employee.save()
                employee_serializer = EmployeeSerializer(employee)
                return Response(employee_serializer.data, status=status.HTTP_200_OK)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployeeDetailAPI(APIView):

    def get_object(self, pk):
        return get_object_or_404(Employee, pk=pk)

    def get(self, request, pk):
        employee = self.get_object(pk)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)

    def put(self, request, pk):
        employee = self.get_object(pk)
        serializer = EmployeeSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        employee = self.get_object(pk)
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SpecializationAPIView(APIView):

    def get(self, request):
        objs: QuerySet[Specialization] = Specialization.objects.filter()
        serializer = SpecializationSerializer(objs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SpecializationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SpecializationDetailAPI(APIView):

    def get_object(self, code):
        return get_object_or_404(Specialization, code=code)

    def get(self, request, code):
        obj = self.get_object(code)
        serializer = SpecializationSerializer(obj)
        return Response(serializer.data)

    def put(self, request, code):
        obj = self.get_object(code)
        serializer = SpecializationSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, code):
        obj = self.get_object(code)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LeaveTypesAPIView(APIView):

    def get(self, request):
        leavetype = LeaveType.objects.filter()
        serializer = LeaveTypeSerializer(leavetype, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = LeaveTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LeaveTypeDetailAPI(APIView):

    def get_object(self, pk):
        return get_object_or_404(LeaveType, pk=pk)

    def get(self, request, pk):
        leavetype = self.get_object(pk)
        serializer = LeaveTypeSerializer(leavetype)
        return Response(serializer.data)

    def put(self, request, pk):
        leavetype = self.get_object(pk)
        serializer = LeaveTypeSerializer(leavetype, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        leavetype = self.get_object(pk)
        leavetype.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LeaveImportAPIView(APIView):
    def post(self, request):
        
        serializer = LeaveImportSerializer(data=request.data)
        
        if serializer.is_valid():
            validated_data:dict = serializer.validated_data
            
            try:
                employee = Employee.objects.get(minoas_id=validated_data.get('minoas_employee_id'))
            except Employee.DoesNotExist:
                return Response({
                    'message': f"Employee {validated_data.get('minoas_employee_id')} could not be found"
                }, status=status.HTTP_404_NOT_FOUND)

            try:
                leave_type = LeaveType.objects.get(minoas_id=validated_data.get('minoas_leave_type_id'))
            except LeaveType.DoesNotExist:
                return Response({
                    'message': f"leave type {validated_data.get('minoas_leave_type_id')} could not be found"
                }, status=status.HTTP_404_NOT_FOUND)

            try:
                leave: Leave = Leave.objects.get(minoas_id=validated_data.get('minoas_id'))
            except Leave.DoesNotExist:
                leave = None

            if leave is None:

                leave = Leave.objects.create(
                    minoas_id=validated_data.get('minoas_id'),
                    employee=employee,
                    leave_type=leave_type,
                    is_active=validated_data.get('is_active'),
                    comment=validated_data.get('comment'),
                    date_from=validated_data.get('date_from'),
                    date_until=validated_data.get('date_until'),
                    effective_number_of_days=validated_data.get('effective_number_of_days'),
                    number_of_days=validated_data.get('number_of_days'),
                    is_deleted=validated_data.get('is_deleted'),
                    deleted_on=validated_data.get('deleted_on'),
                    deleted_comment=validated_data.get('deleted_comment'),
                )

                leave_serializer = LeaveSerializer(leave)
                return Response(leave_serializer.data, status=status.HTTP_201_CREATED)

            else:
                leave.minoas_id = validated_data.get('minoas_id')
                leave.employee = employee
                leave.leave_type = leave_type
                leave.is_active = validated_data.get('is_active')
                leave.comment = validated_data.get('comment')
                leave.date_from = validated_data.get('date_from')
                leave.date_until = validated_data.get('date_until')
                leave.effective_number_of_days = validated_data.get('effective_number_of_days')
                leave.number_of_days = validated_data.get('number_of_days')
                leave.is_deleted = validated_data.get('is_deleted')
                leave.deleted_on = validated_data.get('deleted_on')
                leave.deleted_comment = validated_data.get('deleted_comment')
                leave.save()
                leave_serializer = LeaveSerializer(leave)

                return Response(leave_serializer.data, status=status.HTTP_200_OK)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def merge_employee(employees: QuerySet[Employee]) -> Employee:
    # based on the leaves we will decide which employee will "survive
    latest_leave = None
    logging.warn("trying to merge employees '%s'", employees)

    for employee in employees:

        employee_leaves: QuerySet[Leave] = Leave.objects.filter(employee=employee, is_deleted=False).\
            order_by('-date_until')

        if employee_leaves.count() > 0:
            logging.info("employee '%s' has '%d' leave(s)", employee, employee_leaves.count())

            leave_candidate: Leave = employee_leaves.first()

            if latest_leave is None:
                latest_leave = leave_candidate
                logging.warn("setting leave '%s' of employee '%s' as reference leave", latest_leave, employee)
            else:
                if leave_candidate.date_until > latest_leave.date_until:
                    latest_leave = leave_candidate
                    logging.warn("setting leave '%s' of employee '%s' as reference leave", latest_leave, employee)

        else:
            logging.info("employee '%s' does have leaves", employee)

    if latest_leave is not None:
        reference_employee = latest_leave.employee
    else:
        reference_employee = employees.first()

    with transaction.atomic():
        for employee in employees:

            if employee.pk != reference_employee.pk:
                # transfer leaves to reference employee
                employee_leaves: QuerySet[Leave] = Leave.objects.filter(employee=employee)
                for employee_leave in employee_leaves:
                    employee_leave.employee = reference_employee

                # mark employee as deleted
                employee.is_active = False
                employee.deleted_on = now()
                employee.deleted_comment = "merged with employee '%s'" % employee
                employee.save()

    logging.warn("reference employee is set to '%s'", reference_employee)
    return reference_employee


class AthinaEmployeeImportAPIView(APIView):

    def post(self, request):

        serializer = AthinaEmployeeImportSerializer(data=request.data)

        if serializer.is_valid():

            employee: Employee = None
            employee_type: EmployeeType = None

            validated_data = serializer.validated_data

            employee_first_name = validated_data.get('employee_first_name')
            employee_last_name = validated_data.get('employee_last_name')
            employee_father_name = validated_data.get('employee_father_name')
            employee_mother_name = validated_data.get('employee_mother_name')
            validated_data.get('employee_sex')
            employee_type_name = validated_data.get('employee_type_name')

            employee_specialization = validated_data.get('employee_specialization')
            employee_specialization_name = validated_data.get('employee_specialization_name')
            employee_vat_number = validated_data.get('employee_afm')
            employee_id_number = validated_data.get('employee_adt')
            employee_registry_id = validated_data.get('employee_am')
            employee_amka = validated_data.get('employee_amka')
            employee_date_of_birth = validated_data.get('employee_birthday')
            employee_address_line = validated_data.get('communication_address')
            employee_address_city = validated_data.get('communication_city')
            employee_address_zip = validated_data.get('communication_zip')
            employee_telephone = validated_data.get('communication_telephone')
            employee_fek_diorismou = validated_data.get('employee_fek_diorismou')
            employee_fek_diorismou_date = validated_data.get('employee_fek_diorismou_date')
            validated_data.get('employee_specialization_old')
            validated_data.get('employee_specialization_old_name')

            work_experiences = validated_data.get('work_experience', list())

            athina_employee_label = f'({employee_registry_id}) {employee_last_name} {employee_first_name} ' \
                                    f'{employee_father_name} [{employee_specialization}]'

            logging.info("trying to update employee '%s'", athina_employee_label)

            try:
                employee_legacy_type_code = LegacyEmployeeType.REGULAR

                if employee_type_name == 'Μόνιμος Εκπαιδευτικός':
                    employee_legacy_type_code = LegacyEmployeeType.REGULAR

                employee_type: EmployeeType = EmployeeType.objects.get(athina_code=validated_data.get('employee_type'))
            except EmployeeType.DoesNotExist:
                employee_type = EmployeeType.objects.create(athina_code=validated_data.get('employee_type'),
                                                            title=employee_type_name,
                                                            legacy_type=employee_legacy_type_code)

            # first try to match employee with AM
            employees: QuerySet[Employee] = Employee.objects.filter(
                registry_id=employee_registry_id,
                is_active=True,
                employee_type=employee_legacy_type_code)

            if employees.count() == 1:
                employee: Employee = employees.first()
            elif employees.count() > 1:
                employee: Employee = merge_employee(employees)
            else:
                employee = None

            # if we failed to match, then try with AFM
            if employee is None:

                employees: QuerySet[Employee] = Employee.objects.filter(
                    vat_number=employee_vat_number,
                    is_active=True,
                    employee_type=employee_legacy_type_code)

                if employees.count() == 1:
                    employee = employees.first()
                elif employees.count() > 1:
                    employee: Employee = merge_employee(employees)

            if employee is not None:

                # update operation
                employee.first_name = employee_first_name
                employee.last_name = employee_last_name
                employee.father_name = employee_father_name
                employee.mother_name = employee_mother_name
                validated_data.get('employee_sex')
                employee.employee_type_extended = employee_type

                employee.vat_number = employee_vat_number
                employee.id_number = employee_id_number
                employee.registry_id = employee_registry_id
                employee.amka = employee_amka
                employee.date_of_birth = employee_date_of_birth
                employee.address_line = employee_address_line
                employee.address_city = employee_address_city
                employee.address_zip = employee_address_zip
                employee.telephone = employee_telephone
                employee.fek_diorismou = employee_fek_diorismou
                employee.fek_diorismou_date = employee_fek_diorismou_date

                validated_data.get('employee_specialization_old')
                validated_data.get('employee_specialization_old_name')

                today = now()
                employee.updated_from_athina = today
                employee.updated_on = today
                employee.save()
                employee_serializer = EmployeeSerializer(employee)
                logging.info("employee '%s' updated", athina_employee_label)

                # work experience handling
                WorkExperience.objects.filter(employee=employee).delete()
                for work_experience in work_experiences:
                    work_experience_work_type = work_experience.get('work_type')
                    work_experience_work_type_name = work_experience.get('work_type_name')

                    try:
                        work_experience_type = WorkExperienceType.objects.get(code=work_experience_work_type)
                    except WorkExperienceType.DoesNotExist:
                        work_experience_type = WorkExperienceType.objects.create(
                            code=work_experience_work_type,
                            description=work_experience_work_type_name)

                    work_experience_work_duration_str: str = work_experience.get('work_duration')
                    work_experience_elements = work_experience_work_duration_str.split(':')

                    if len(work_experience_elements) != 3:

                        logging.warning('work experience "%s" for employee "%s" could not be decoded',
                                        work_experience_work_duration_str, athina_employee_label)
                        work_experience_duration_days = 0
                        work_experience_duration_months = 0
                        work_experience_duration_years = 0

                    else:
                        work_experience_duration_days = int(work_experience_elements[2])
                        work_experience_duration_months = int(work_experience_elements[1])
                        work_experience_duration_years = int(work_experience_elements[0])

                    work_experience_work_duration = work_experience_duration_years * 360 + \
                                                    work_experience_duration_months * 30 + \
                                                    work_experience_duration_days

                    work_experience_document_number = work_experience.get('document_number')
                    work_experience_document_date = work_experience.get('document_date')
                    work_experience_authority = work_experience.get('authority')
                    work_experience_work_from = work_experience.get('work_from')
                    work_experience_work_until = work_experience.get('work_until')
                    work_experience_work_comment = work_experience.get('work_comment')

                    WorkExperience.objects.create(
                        employee=employee,
                        work_experience_type=work_experience_type,
                        duration_total_in_days=work_experience_work_duration,
                        duration_days=work_experience_duration_days,
                        duration_months=work_experience_duration_months,
                        duration_years=work_experience_duration_years,
                        document_number=work_experience_document_number,
                        document_date=work_experience_document_date,
                        authority=work_experience_authority,
                        date_from=work_experience_work_from,
                        date_until=work_experience_work_until,
                        comment=work_experience_work_comment,
                    )

                return Response(employee_serializer.data, status=status.HTTP_200_OK)
            else:
                # employee not found
                logging.warning("employee '%s' NOT FOUND in phaistos, will create a new one", athina_employee_label)
                employee = Employee.objects.create(
                    first_name=employee_first_name,
                    last_name=employee_last_name,
                    father_name=employee_father_name,
                    mother_name=employee_mother_name,
                    employee_type_extended=employee_type,
                    vat_number=employee_vat_number,
                    id_number=employee_id_number,
                    registry_id=employee_registry_id,
                    amka=employee_amka,
                    date_of_birth=employee_date_of_birth,
                    address_line=employee_address_line,
                    address_city=employee_address_city,
                    address_zip=employee_address_zip,
                    telephone=employee_telephone,
                    imported_from_athina=now()
                )
                employee.save()
                employee_serializer = EmployeeSerializer(employee)
                return Response(employee_serializer.data, status=status.HTTP_201_CREATED)

        #     employee_serializer = EmployeeSerializer(employee)
        #     return Response(employee_serializer.data, status=status.HTTP_200_OK)
            # try:
            #     specialization: Specialization = Specialization.objects.get(
            #         code=validated_data.get('specialization_code'))
            # except Specialization.DoesNotExist:
            #     specialization = None
            #
            # try:
            #     employee: Employee = Employee.objects.get(minoas_id=validated_data.get('minoas_id'))
            # except Employee.DoesNotExist:
            #     employee = None
            #
            # current_unit_id = validated_data.get('current_unit_id')
            # if current_unit_id is not None:
            #     try:
            #         current_unit = Unit.objects.get(minoas_id=current_unit_id)
            #     except Unit.DoesNotExist:
            #         current_unit = None
            # else:
            #     current_unit = None
            #
            # if employee is None:
            #
            #     employee = Employee.objects.create(
            #         minoas_id=validated_data.get('minoas_id'),
            #         big_family=validated_data.get('big_family'),
            #         comment=validated_data.get('comment'),
            #         date_of_birth=validated_data.get('date_of_birth'),
            #         email=validated_data.get('email'),
            #         father_name=validated_data.get('father_name'),
            #         father_surname=validated_data.get('father_surname'),
            #         first_name=validated_data.get('first_name'),
            #         last_name=validated_data.get('last_name'),
            #         id_number=validated_data.get('id_number'),
            #         id_number_authority=validated_data.get('id_number_authority'),
            #         is_man=validated_data.get('is_man'),
            #         mother_name=validated_data.get('mother_name'),
            #         mother_surname=validated_data.get('mother_surname'),
            #         vat_number=validated_data.get('vat_number'),
            #         employee_type=validated_data.get('employee_type'),
            #         marital_status=validated_data.get('marital_status'),
            #         specialization=specialization,
            #         registry_id=validated_data.get('registry_id'),
            #         current_unit=current_unit,
            #         is_active=validated_data.get('is_active')
            #     )
            #
            #     employee_serializer = EmployeeSerializer(employee)
            #     return Response(employee_serializer.data, status=status.HTTP_201_CREATED)
            #
            # else:
            #     employee.big_family = validated_data.get('big_family')
            #     employee.comment = validated_data.get('comment')
            #     employee.date_of_birth = validated_data.get('date_of_birth')
            #     employee.email = validated_data.get('email')
            #     employee.father_name = validated_data.get('father_name')
            #     employee.father_surname = validated_data.get('father_surname')
            #     employee.first_name = validated_data.get('first_name')
            #     employee.last_name = validated_data.get('last_name')
            #     employee.id_number = validated_data.get('id_number')
            #     employee.id_number_authority = validated_data.get('id_number_authority')
            #     employee.is_man = validated_data.get('is_man')
            #     employee.mother_name = validated_data.get('mother_name')
            #     employee.mother_surname = validated_data.get('mother_surname')
            #     employee.vat_number = validated_data.get('vat_number')
            #     employee.employee_type = validated_data.get('employee_type')
            #     employee.marital_status = validated_data.get('marital_status')
            #     employee.specialization = specialization
            #     employee.registry_id = validated_data.get('registry_id')
            #     employee.current_unit = current_unit
            #     employee.is_active = validated_data.get('is_active')
            #
            #     employee.save()
            #     employee_serializer = EmployeeSerializer(employee)
            #     return Response(employee_serializer.data, status=status.HTTP_200_OK)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MySchoolEmployeeImportAPIView(APIView):

    def post(self, request):

        serializer = MySchoolEmployeeImportSerializer(data=request.data)

        if serializer.is_valid() is False:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        employee: Employee = None
        employee_type: EmployeeType = None

        validated_data = serializer.validated_data

        employee_first_name = validated_data.get('employee_first_name')
        employee_last_name = validated_data.get('employee_last_name')
        employee_father_name = validated_data.get('employee_father_name')
        employee_mother_name = validated_data.get('employee_mother_name')
        employee_email = validated_data.get('employee_email')
        employee_email_psd = validated_data.get('employee_email_psd')
        employee_sex = validated_data.get('employee_sex')
        employee_type_name: str = validated_data.get('employee_type_name')
        employee_birthday = validated_data.get('employee_birthday')
        employee_specialization_id = validated_data.get('employee_specialization_id')
        employee_specialization_name = validated_data.get('employee_specialization_name')
        employee_vat_number = validated_data.get('employee_afm')
        employee_registry_id = validated_data.get('employee_am')
        employee_fek_diorismou = validated_data.get('employee_fek_diorismou')
        employee_fek_diorismou_date = validated_data.get('employee_fek_diorismou_date')
        employee_mk = validated_data.get('employee_mk')
        employee_bathmos = validated_data.get('employee_bathmos')
        employee_mandatory_week_workhours = validated_data.get('employee_mandatory_week_workhours')
        employee_first_workday_date = validated_data.get('employee_first_workday_date')
        employee_current_unit_id = validated_data.get('employee_current_unit_id')
        employee_current_unit_name = validated_data.get('employee_current_unit_name')

        employee_communication_telephone = validated_data.get('employee_telephone')
        employee_communication_mobile = validated_data.get('employee_mobile')

        employee_is_man = True if employee_sex == 'Α' else False

        myschool_employee_label = f'({employee_registry_id}) {employee_last_name} {employee_first_name} ' \
                                f'{employee_father_name} [{employee_specialization_id}]'

        # if the employee is "REGULAR" then require employee_registry_id
        if len(employee_registry_id.strip()) == 0 and employee_type_name == 'Μόνιμος':
            raise ValidationError("AM is required")

        with transaction.atomic():

            try:
                employee_specialization = get_cached_employee_specialization(employee_specialization_id)
            except Specialization.DoesNotExist:
                employee_specialization = None

            if employee_specialization is None:
                # we failed to find the specialization. Perhaps the code was the legacy coce, ie "ΠΕ02"
                # and we have stored (in the db) the old type, ie "ΠΕ0201"

                employee_specialization_id_normalized = employee_specialization_id + "01"
                try:
                    employee_specialization = get_cached_employee_specialization(employee_specialization_id_normalized)
                except Specialization.DoesNotExist:
                    employee_specialization = None

            if employee_specialization is None:
                # failed to create specialization, go ahead and create a new one
                employee_specialization: Specialization = Specialization.objects.create(
                    code=employee_specialization_id,
                    title=employee_specialization_name
                )
                logging.error(f'specialization {employee_specialization_id} created !')

            if employee_specialization.title != employee_specialization_name:
                employee_specialization.title = employee_specialization_name
                employee_specialization.save()

            if employee_specialization.code != employee_specialization_id:
                employee_specialization.code = employee_specialization_id
                employee_specialization.save()

            try:
                employee_current_unit: Unit = get_cached_unit(employee_current_unit_id)
            except Unit.DoesNotExist:
                employee_current_unit: Unit = Unit.objects.create(
                    ministry_code=employee_current_unit_id,
                    title=employee_current_unit_name,
                    myschool_title=employee_current_unit_name,
                )
                logging.error(f'******* created unit {employee_current_unit_id} - {employee_current_unit_name}')

            if employee_current_unit.myschool_title != employee_current_unit_name:
                employee_current_unit.myschool_title = employee_current_unit_name
                employee_current_unit.save()

            try:
                if employee_type_name == 'Μόνιμος':
                    employee_legacy_type_code = LegacyEmployeeType.REGULAR
                elif employee_type_name.startswith('Αναπληρωτής'):
                    employee_legacy_type_code = LegacyEmployeeType.DEPUTY
                elif employee_type_name.startswith('Ωρομίσθιος'):
                    employee_legacy_type_code = LegacyEmployeeType.HOURLYPAID
                elif employee_type_name.startswith('Διοικητικός'):
                    employee_legacy_type_code = LegacyEmployeeType.ADMINISTRATIVE
                else:
                    raise ValidationError(f"unsupported employee type '{employee_type_name}'")

                employee_type: EmployeeType = get_cached_employee_type(employee_type_name)

            except EmployeeType.DoesNotExist:
                employee_type = EmployeeType.objects.create(title=employee_type_name,
                                                            legacy_type=employee_legacy_type_code)

            # first try to match employee with AM
            employees: QuerySet[Employee] = Employee.objects.filter(
                registry_id=employee_registry_id,
                is_active=True,
                employee_type=employee_type.legacy_type)

            if employees.count() == 1:
                employee: Employee = employees.first()
            elif employees.count() > 1:
                employee: Employee = merge_employee(employees)
            else:
                employee = None

            # if we failed to match, then try with AFM
            if employee is None:

                employees: QuerySet[Employee] = Employee.objects.filter(
                    vat_number=employee_vat_number,
                    is_active=True,
                    employee_type=employee_type.legacy_type)

                if employees.count() == 1:
                    employee = employees.first()
                elif employees.count() > 1:
                    #employee: Employee = merge_employee(employees)
                    employee = employees.first()

            if employee is not None:

                today = now()

                employee_update_dict = {
                    'vat_number': employee_vat_number,
                    'registry_id': employee_registry_id,
                    'first_name': employee_first_name,
                    'last_name': employee_last_name,
                    'father_name': employee_father_name,
                    'mother_name': employee_mother_name,
                    'date_of_birth': employee_birthday,
                    'email': employee_email,
                    'email_psd': employee_email_psd,
                    'specialization': employee_specialization,
                    'current_unit': employee_current_unit,
                    'telephone': employee_communication_telephone,
                    'mobile': employee_communication_mobile,
                    'fek_diorismou': employee_fek_diorismou,
                    'fek_diorismou_date': employee_fek_diorismou_date,
                    'mk': employee_mk,
                    'bathmos': employee_bathmos,
                    'first_workday_date': employee_first_workday_date,
                    'is_man': employee_is_man,
                    'mandatory_week_workhours': employee_mandatory_week_workhours,
                    'updated_from_myschool': today,
                    'updated_on': today
                }

                for attr, value in employee_update_dict.items():
                    setattr(employee, attr, value)

                #Employee.objects.filter(pk=employee.pk).update(**employee_update_dict)
                employee.save()
                employee_serializer = EmployeeSerializer(employee)
                logging.info("employee [%s] '%s' updated", employee.pk, myschool_employee_label)

                return Response(employee_serializer.data, status=status.HTTP_200_OK)
            else:
                # employee not found
                logging.warning("employee '%s' NOT FOUND in phaistos, will create a new one", myschool_employee_label)

                today = now()

                employee_update_dict = {
                    'vat_number': employee_vat_number,
                    'registry_id': employee_registry_id,
                    'first_name': employee_first_name,
                    'last_name': employee_last_name,
                    'father_name': employee_father_name,
                    'mother_name': employee_mother_name,
                    'date_of_birth': employee_birthday,
                    'email': employee_email,
                    'email_psd': employee_email_psd,
                    'specialization': employee_specialization,
                    'current_unit': employee_current_unit,
                    'telephone': employee_communication_telephone,
                    'mobile': employee_communication_mobile,
                    'employee_type': employee_type.legacy_type,
                    'employee_type_extended': employee_type,
                    'fek_diorismou': employee_fek_diorismou,
                    'fek_diorismou_date': employee_fek_diorismou_date,
                    'mk': employee_mk,
                    'bathmos': employee_bathmos,
                    'first_workday_date': employee_first_workday_date,
                    'is_man': employee_is_man,
                    'mandatory_week_workhours': employee_mandatory_week_workhours,
                    'imported_from_myschool': today,
                    'created_on': today
                }

                employee = Employee.objects.create(**employee_update_dict)
                employee_serializer = EmployeeSerializer(employee)
                return Response(employee_serializer.data, status=status.HTTP_201_CREATED)


class MySchoolEmploymentImportAPIView(APIView):

    def post(self, request):

        serializer = MySchoolEmploymentImportSerializer(data=request.data)

        if serializer.is_valid() is False:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data

        employee_afm = validated_data.get('employee_afm')
        employee_am = validated_data.get('employee_am')
        employee_last_name = validated_data.get('employee_last_name')
        employee_first_name = validated_data.get('employee_first_name')
        employee_employment_unit_id = validated_data.get('employee_employment_unit_id')
        employee_employment_unit_name = validated_data.get('employee_employment_unit_name')
        employee_specialization_id = validated_data.get('employee_specialization_id')
        employee_type_str: str = validated_data.get('employee_type')
        employee_employment_type = validated_data.get('employee_employment_type')
        employee_employment_days = validated_data.get('employee_employment_days')
        employee_employment_hours = validated_data.get('employee_employment_hours')
        employee_employment_from = validated_data.get('employee_employment_from')
        employee_employment_until = validated_data.get('employee_employment_until')
        employee_employment_status = validated_data.get('employee_employment_status')


        myschool_employment_label = f'({employee_am}/{employee_am}) {employee_last_name} {employee_first_name} ' \
                                f'[{employee_specialization_id}]'

        with transaction.atomic():

            try:
                if employee_type_str == 'Μόνιμος':
                    legacy_employee_type_code = LegacyEmployeeType.REGULAR
                elif employee_type_str.startswith('Αναπληρωτής'):
                    legacy_employee_type_code = LegacyEmployeeType.DEPUTY
                elif employee_type_str.startswith('Ωρομίσθιος'):
                    legacy_employee_type_code = LegacyEmployeeType.HOURLYPAID
                elif employee_type_str.startswith('Διοικητικός'):
                    legacy_employee_type_code = LegacyEmployeeType.ADMINISTRATIVE
                elif employee_type_str == 'Ιδιωτικού Δικαίου Αορίστου Χρόνου (Ι.Δ.Α.Χ.)':
                    legacy_employee_type_code = LegacyEmployeeType.IDAX
                else:
                    raise ValidationError(f"unsupported employee type '{employee_type_str}'")

                employee_type: EmployeeType = get_cached_employee_type(employee_type_str)

            except EmployeeType.DoesNotExist:
                employee_type = EmployeeType.objects.create(title=employee_type_str,
                                                            legacy_type=legacy_employee_type_code)

            try:
                employment_type = get_cached_employment_type(employee_employment_type)
            except EmploymentType.DoesNotExist:

                employment_type = EmploymentType.objects.create(title=employee_employment_type)

            try:
                employee_specialization = get_cached_employee_specialization(employee_specialization_id)
            except Specialization.DoesNotExist:
                employee_specialization = None

            if employee_specialization is None:
                # we failed to find the specialization. Perhaps the code was the legacy coce, ie "ΠΕ02"
                # and we have stored (in the db) the old type, ie "ΠΕ0201"

                employee_specialization_id_normalized = employee_specialization_id + "01"
                try:
                    employee_specialization = get_cached_employee_specialization(employee_specialization_id_normalized)
                except Specialization.DoesNotExist:
                    employee_specialization = None

            if employee_specialization is None:
                # failed to create specialization, go ahead and create a new one
                employee_specialization: Specialization = Specialization.objects.create(
                    code=employee_specialization_id,
                    title=''
                )
                logging.error(f'specialization {employee_specialization_id} created !')

            if employee_specialization.code != employee_specialization_id:
                employee_specialization.code = employee_specialization_id
                employee_specialization.save()

            try:
                employment_unit: Unit = get_cached_unit(employee_employment_unit_id)
            except Unit.DoesNotExist:
                employment_unit: Unit = Unit.objects.create(
                    ministry_code=employee_employment_unit_id,
                    title=employee_employment_unit_name,
                    myschool_title=employee_employment_unit_name,
                )
                logging.error(f'******* created unit {employee_employment_unit_id} - {employee_employment_unit_name}')

            if employment_unit.myschool_title != employee_employment_unit_name:
                employment_unit.myschool_title = employee_employment_unit_name
                employment_unit.save()

            # first try to match employee with AM
            employee = None

            if len(employee_am) > 0:
                employees: QuerySet[Employee] = Employee.objects.filter(
                    registry_id=employee_am,
                    is_active=True,
                    employee_type=employee_type.legacy_type)

                if employees.count() == 1:
                    employee: Employee = employees.first()
                elif employees.count() > 1:
                    employee: Employee = merge_employee(employees)

            # if we failed to match, then try with AFM
            if employee is None and len(employee_afm) > 0:
                employees: QuerySet[Employee] = Employee.objects.filter(
                    vat_number=employee_afm,
                    is_active=True,
                    employee_type=employee_type.legacy_type)

                if employees.count() == 1:
                    employee = employees.first()
                elif employees.count() > 1:
                    employee: Employee = merge_employee(employees)

            today = now()

            if employee is None:
                # employee not found

                employee_dict = {
                    'vat_number': employee_afm,
                    'registry_id': employee_am,
                    'first_name': employee_first_name,
                    'last_name': employee_last_name,
                    'specialization': employee_specialization,
                    'current_unit': employment_unit,
                    'employee_type': employee_type.legacy_type,
                    'employee_type_extended': employee_type,
                    'imported_from_myschool': today,
                    'created_on': today
                }
                employee = Employee.objects.create(**employee_dict)

            employment_dict = {
                'employee': employee,
                'specialization': employee_specialization,
                'current_unit': employment_unit,
                'school_year': SchoolYear.get_or_create_school_year(reference_date=employee_employment_from),
                'employment_type': employee_type.legacy_type,
                'employment_type_extended': employment_type,
                'is_active': employee_employment_status == 'ΠΑΡΟΥΣΙΑ',
                'myschool_status': employee_employment_status,
                'mandatory_week_workhours': employee_employment_hours,
                'week_workdays': employee_employment_days,
                'effective_from': employee_employment_from,
                'effective_until': employee_employment_until,
                'praksi_topothetisis': '',
                'praksi_topothetisis_date': None,
                'imported_from_myschool': today,
            }

            employement: Employment = Employment.objects.create(**employment_dict)

            # check if we need to update the employee's current unit
            if employment_type.title == 'Οργανικά' and employement.is_active is True:
                employee.current_unit = employement.current_unit
                employement.save()

            employment_serializer = EmploymentSerializer(employement)
            return Response(employment_serializer.data, status=status.HTTP_201_CREATED)


class SubstituteEmploymentAnnouncementImportAPIView(APIView):

    def post(self, request):

        serializer = SubstituteEmploymentAnnouncementImportSerializer(data=request.data)

        if serializer.is_valid() is False:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data

        employee_afm = validated_data.get('employee_afm')
        employee_last_name = validated_data.get('employee_last_name')
        employee_first_name = validated_data.get('employee_first_name')
        employee_father_name = validated_data.get('employee_father_name')
        employee_mother_name = validated_data.get('employee_mother_name')
        employee_specialization_id = validated_data.get('employee_specialization_id')
        financing_source_code = validated_data.get('financing_source_code')
        employment_source_code = validated_data.get('employment_source_code')
        employment_table = validated_data.get('employment_table')
        employment_table_position = validated_data.get('employment_table_position')
        employment_table_score = validated_data.get('employment_table_score')
        employee_address_city = validated_data.get('employee_address_city')
        employee_address_line = validated_data.get('employee_address_line')
        employee_address_postal_code = validated_data.get('employee_address_postal_code')
        employee_telephone = validated_data.get('employee_telephone')
        employee_mobile = validated_data.get('employee_mobile')
        employee_email = validated_data.get('employee_email')
        # 'employee_birthday': _employee_birthday,
        employee_adt = validated_data.get('employee_adt')
        print(validated_data)

        with transaction.atomic():
            legacy_employee_type_code = LegacyEmployeeType.DEPUTY

            #                                                 legacy_type=legacy_employee_type_code)

            financing_source = EmploymentFinancialSource.get_or_create(code=financing_source_code)
            employment_source = SubstituteEmploymentSource.get_or_create(code=employment_source_code)

            try:
                employee_specialization = get_cached_employee_specialization(employee_specialization_id)
            except Specialization.DoesNotExist:
                employee_specialization = None

            if employee_specialization is None:
                # we failed to find the specialization. Perhaps the code was the legacy coce, ie "ΠΕ02"
                # and we have stored (in the db) the old type, ie "ΠΕ0201"

                employee_specialization_id_normalized = employee_specialization_id + "01"
                try:
                    employee_specialization = get_cached_employee_specialization(employee_specialization_id_normalized)
                except Specialization.DoesNotExist:
                    employee_specialization = None

            if employee_specialization is None:
                # failed to create specialization, go ahead and create a new one
                employee_specialization: Specialization = Specialization.objects.create(
                    code=employee_specialization_id,
                    title=''
                )
                logging.error(f'specialization {employee_specialization_id} created !')

            today = now()

            employee, employee_created = Employee.objects.update_or_create(
                vat_number=employee_afm, is_active=True,
                defaults={
                    'vat_number': employee_afm,
                    'first_name': employee_first_name,
                    'last_name': employee_last_name,
                    'father_name': employee_father_name,
                    'mother_name': employee_mother_name,
                    'address_line': employee_address_line,
                    'address_city': employee_address_city,
                    'address_zip': employee_address_postal_code,
                    'telephone': employee_telephone,
                    'mobile': employee_mobile,
                    'email': employee_email,
                    'adt': employee_adt,
                    'specialization': employee_specialization,
                    'updated_on': today,
                    'employee_type': legacy_employee_type_code,
                }
            )

            if employee_created is True:
                employee.created_on = today
                employee.save()




            sea: SubstituteEmploymentAnnouncement = SubstituteEmploymentAnnouncement.objects.create(
                employee=employee,
                specialization=employee_specialization,
                school_year=SchoolYear.get_current_school_year(),
                financing=financing_source,
                employment_source=employment_source,
                table=employment_table,
                table_rank=employment_table_position,
                table_points=employment_table_score
            )

            # employment_dict = {
            #     'employee': employee,
            #     'specialization': employee_specialization,
            #     'current_unit': employment_unit,
            #     'school_year': SchoolYear.get_or_create_school_year(reference_date=employee_employment_from),
            #     'employment_type': employee_type.legacy_type,
            #     'employment_type_extended': employment_type,
            #     'is_active': employee_employment_status == 'ΠΑΡΟΥΣΙΑ',
            #     'myschool_status': employee_employment_status,
            #     'mandatory_week_workhours': employee_employment_hours,
            #     'week_workdays': employee_employment_days,
            #     'effective_from': employee_employment_from,
            #     'effective_until': employee_employment_until,
            #     'praksi_topothetisis': '',
            #     'praksi_topothetisis_date': None,
            #     'imported_from_myschool': today,
            # }
            #
            # employement: Employment = Employment.objects.create(**employment_dict)

            # check if we need to update the employee's current unit

            employment_serializer = EmploymentSerializer({})
            return Response({}, status=status.HTTP_201_CREATED)









