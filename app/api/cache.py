import logging

from functools import lru_cache
from employees.models import EmployeeType, Specialization, Unit, EmploymentType


@lru_cache()
def get_cached_employee_type(employee_type_title) -> EmployeeType:
    return EmployeeType.objects.get(title=employee_type_title)


@lru_cache()
def get_cached_employee_specialization(specialization_code) -> Specialization:
    return Specialization.objects.get(code=specialization_code)


@lru_cache(maxsize=200)
def get_cached_unit(unit_id) -> Unit:
    try:
        return Unit.objects.get(ministry_code=unit_id)
    except Unit.MultipleObjectsReturned:
        logging.warning(f'unit {unit_id} is duplicate in phaistos')
        return Unit.objects.filter(ministry_code=unit_id).order_by('title').first()


@lru_cache(maxsize=200)
def get_cached_employment_type(employment_type_name) -> EmploymentType:
    return EmploymentType.objects.get(title=employment_type_name)
