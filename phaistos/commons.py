from django.db.models import Q
from datetime import date
from leaves.models import Leave
from employees.models import Employee
from typing import List

# taken directly from minoas code
REGULAR_TYPE_LEAVE_TYPES = ["31", "54", "74", ]

# taken directly from minoas code
MEDICAL_TYPE_LEAVE_TYPES = ["41", "42", "47", "48", "55", "71", ]


def compute_leaves_real_duration(leaves: List[Leave], trim_to_year=None):
    """
    Computes the real duration of a list of leaves.
    :param leaves:
    :param trim_to_year:
    :return:
    """

    if trim_to_year is not None:
        # we don't support the feature yet
        raise RuntimeError("trim_to_year feature is not supported yet")

    leaves_duration = 0
    for leave in leaves:
        print(leave)
        print(leave.leave_type)
        print(leave.effective_number_of_days)
        print(leave.is_deleted)
        print(leave.employee)
        leaves_duration += leave.effective_number_of_days
    print(leaves_duration)
    return leaves_duration


def get_regular_leaves_for_employee_established_in_year(employee: Employee,
                                                        year: int = None, year_from: int = None, year_until: int = None) -> List[Leave]:
    """
    Return "regular" leaves for an employee
    :param employee:
    :param year:
    :param year_from:
    :param year_until:
    :return:
    """
    if year_from and year_until:
        start_of_year = date(year=year_from, month=1, day=1)
        end_of_year = start_of_year.replace(year=year_until, month=12, day=31)
    elif year:
        start_of_year = date(year=year, month=1, day=1)
        end_of_year = start_of_year.replace(month=12, day=31)
    else:
        raise RuntimeError("wrong combination of year, year_from and year_until options provided")

    date_range = [start_of_year, end_of_year]
    return Leave.objects.filter(employee=employee,
                                is_deleted=False,
                                leave_type__legacy_code__in=REGULAR_TYPE_LEAVE_TYPES).\
        filter(Q(date_from__range=date_range) | Q(date_until__range=date_range))


def get_medical_leaves_for_employee_established_in_year(employee: Employee,
                                                        year: int = None, year_from: int = None, year_until: int = None) -> List[Leave]:
    """
        Return "medical" leaves for an employee
        :param employee:
        :param year:
        :param year_from:
        :param year_until:
        :return:
        """
    if year_from and year_until:
        start_of_year = date(year=year_from, month=1, day=1)
        end_of_year = start_of_year.replace(year=year_until, month=12, day=31)
    elif year:
        start_of_year = date(year=year, month=1, day=1)
        end_of_year = start_of_year.replace(month=12, day=31)
    else:
        raise RuntimeError("wrong combination of year, year_from and year_until options provided")

    date_range = [start_of_year, end_of_year]
    return Leave.objects.filter(employee=employee,
                                is_deleted=False,
                                leave_type__legacy_code__in=MEDICAL_TYPE_LEAVE_TYPES). \
        filter(Q(date_from__range=date_range) | Q(date_until__range=date_range))

