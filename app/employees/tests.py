import uuid

from django.contrib.auth.models import Permission
from django.db import connection
from django.test import TestCase
from django.urls import reverse

from employees.models import Employee, LegacyEmployeeType
from users.models import CustomUser as User


class EmployeeUUIDTest(TestCase):
    """
    Regression tests for UUID handling on MariaDB 10.7+, where Django 5.0+ would otherwise send
    dashed UUIDs that don't match the existing char(32) columns.
    """

    @classmethod
    def setUpTestData(cls):
        cls.employee = Employee.objects.create(
            first_name="ΔΟΚΙΜΙΟΣ",
            last_name="ΔΟΚΙΜΟΠΟΥΛΟΣ",
            father_name="ΜΠΑΜΠΑΣ",
            employee_type=LegacyEmployeeType.REGULAR,
        )
        cls.user = User.objects.create_user(username="viewer", password="pass")
        cls.user.user_permissions.add(Permission.objects.get(codename="view_employee"))

    def test_uuid_is_stored_as_32_char_hex(self):
        table = Employee._meta.db_table
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT uuid FROM {connection.ops.quote_name(table)} WHERE id = %s",
                           [self.employee.pk])
            (stored,) = cursor.fetchone()
        self.assertEqual(str(stored), self.employee.uuid.hex)

    def test_lookup_by_uuid(self):
        for value in (self.employee.uuid, str(self.employee.uuid), self.employee.uuid.hex):
            with self.subTest(value=value):
                self.assertEqual(Employee.objects.get(uuid=value), self.employee)

    def test_lookup_by_unknown_uuid(self):
        self.assertFalse(Employee.objects.filter(uuid=uuid.uuid4()).exists())

    def test_detail_view(self):
        self.client.login(username="viewer", password="pass")
        response = self.client.get(reverse("employees:employee-detail", kwargs={"uuid": self.employee.uuid}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["object"], self.employee)
