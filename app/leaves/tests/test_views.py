from contextlib import redirect_stderr

from django.test import TestCase
from django.urls import reverse
from django.forms import BaseForm
from employees.models import Specialization, LegacyEmployeeType, Employee
from leaves.models import Leave, LeaveType
from leaves.models import Leave
from django.contrib.auth.models import Permission
from users.models import CustomUser as User
from datetime import datetime


# more info https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Testing
class LeaveCreateViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):

        can_add_leave_user: User = User.objects.create_user(username="can_add_leave_user", password='pass')

        can_add_leave_perm = Permission.objects.get(name='Can add leave')
        can_delete_leave_perm = Permission.objects.get(name='Can delete leave')
        can_change_leave_perm = Permission.objects.get(name='Can change leave')

        # give permissions to add/delete/change leaves to user 'can_add_leave_user'
        can_add_leave_user.user_permissions.add(can_add_leave_perm)
        can_add_leave_user.user_permissions.add(can_delete_leave_perm)
        can_add_leave_user.save()

        # create some leave types
        LeaveType.objects.create(legacy_code='1', suitable_for_employee_type=LegacyEmployeeType.REGULAR)

        sp: Specialization = Specialization.objects.create(
                    code='ΠΕ86',
                    title="ΚΑΠΟΙΟΣ ΤΙΤΛΟΣ"
                )

        employee: Employee = Employee.objects.create(
            first_name="ΔΟΚΙΜΙΟΣ",
            last_name="ΔΟΚΙΜΟΠΟΥΛΟΣ",
            father_name="ΜΠΑΜΠΑΣ",
            employee_type=LegacyEmployeeType.REGULAR,
            specialization=sp
        )

    def test_create_leave_view(self):
        login = self.client.login(username='can_add_leave_user', password='pass')
        employee = Employee.objects.get(id=1)

        # no leaves should be available
        self.assertEqual(Leave.objects.all().count(), 0)

        response = self.client.post(
            reverse('leaves:leave-create', kwargs={'employee_uuid': employee.uuid}),
            data={
                'number_of_days': 1,
                'effective_number_of_days': 1,
                'leave_type': 1,
                'date_from': '2023-12-01',
                'date_until': '2023-12-20',
                'comment': ''
            },
        )

        # the form redirects to
        self.assertEqual(response.status_code, 302)

        # we should have a leave
        self.assertEqual(Leave.objects.all().count(), 1)

    def test_delete_leave_view(self):
        login = self.client.login(username='can_add_leave_user', password='pass')

        employee: Employee = Employee.objects.get(id=1)
        leave_type: LeaveType = LeaveType.objects.get(id=1)

        # add a leave
        leave: Employee = Leave.objects.create(
            employee=employee,
            date_from=datetime.utcnow(),
            date_until=datetime.utcnow(),
            leave_type=leave_type
        )

        # we should have a leave
        self.assertEqual(Leave.objects.all().count(), 1)

        self.assertTrue(leave.is_active)
        self.assertFalse(leave.deleted_on)
        self.assertIsNone(leave.deleted_comment)

        response = self.client.post(
            reverse('leaves:leave-delete', kwargs={'pk': leave.pk}),
            data={
                'deleted_comment': 'Το σβήσαμε'
            },
        )

        self.assertEqual(response.status_code, 302)

        # we should still have the leave
        self.assertEqual(Leave.objects.all().count(), 1)

        # re-read the leave from db
        leave.refresh_from_db()

        self.assertFalse(leave.is_active)
        self.assertTrue(leave.deleted_on)
        self.assertEqual(leave.deleted_comment, 'Το σβήσαμε')




