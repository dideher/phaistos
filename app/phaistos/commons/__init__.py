from django.db.models import Q
from datetime import date
from leaves.models import Leave
from employees.models import Employee
from typing import List
import calendar

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
        leaves_duration += leave.effective_number_of_days
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


def days360(start_date, end_date, include_last_lay=False):
    """
    Taken from https://github.com/dideher/certificate_of_employment/blob/master/certificate_of_employment/state_funded_associate_professors/days360.py#L6
    :param start_date:
    :param end_date:
    :param include_last_lay: If set to true, then the result will be increased by just one day
    :return:
    """
    # method_eu = False

    start_day = start_date.day
    start_month = start_date.month
    start_year = start_date.year

    end_day = end_date.day
    end_month = end_date.month
    end_year = end_date.year

    start_day_is_last_of_February = (start_month == 2 and start_day == 29) or (
                start_month == 2 and start_day == 28 and calendar.isleap(start_year) is False)
    # end_day_is_last_of_February = end_day == 31 or (end_month == 2 and end_day == 29) or
    # (end_month == 2 and end_day == 28 and calendar.isleap(start_year) is False)

    # months_with_31_days = {1, 3, 5, 7, 8, 10, 12}
    # months_with_30_days = {4, 6, 9, 11}
    # end_day_is_last_of_month = (end_day == 31 and end_month in months_with_31_days) or
    # (end_day == 30 and end_month in months_with_30_days)
    # start_day_is_last_of_month = (start_day == 31 and start_month in months_with_31_days) or
    # (start_day == 30 and start_month in months_with_30_days)

    if start_day == 31 or start_day_is_last_of_February:
        start_day = 30

    if start_day == 30 and end_day == 31:
        end_day = 30

    # if end_day_is_last_of_month or end_day_is_last_of_February:
    #   if start_day_is_last_of_month or start_day_is_last_of_February:
    #     end_day = 1
    #     if end_month == 12:
    #       end_year += 1
    #       end_month = 1
    #     else:
    #       end_month += 1
    #   else:
    #     end_day = 30

    result = (end_year - start_year) * 360 + (end_month - start_month) * 30 + end_day - start_day

    return result + 1 if include_last_lay else result