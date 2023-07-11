from rest_framework.exceptions import APIException
from django.utils.translation import gettext_lazy as _
from rest_framework import status


class SubstituteEmploymentAnnouncementNotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = _('Substitute Employment Announcement Not Found')
    default_code = 'announcement_not_found'


class UnitNotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = _('Unit Not Found')
    default_code = 'unit_not_found'


class EmploymentConflictError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Employment Conflict Error')
    default_code = 'employment_conflict_error'
