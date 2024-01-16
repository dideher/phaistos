from django.core.management.base import BaseCommand, CommandError
from employees.models import Employment, Employee, LegacyEmployeeType
from leaves.models import Leave, LeaveType


class Command(BaseCommand):

    def add_arguments(self, parser):

        parser.add_argument(
            "--employee_afm",
            help="employee afm",
        )

        parser.add_argument(
            "--dry_run",
            action="store_true",
            help="enable dry run mode",
        )



        # parser.add_argument(
        #     "--delete",
        #     action="store_true",
        #     help="actually delete duplicate employee",
        # )

    def find_merge_candidate(self, employee: Employee):

        # first check with employee AFM
        if employee.vat_number is not None:

            employee_vat_number: str = employee.vat_number

            if len(employee_vat_number.strip()) == 0:
                employee_vat_number = None
        else:
            employee_vat_number = None

        if employee_vat_number is not None:
            try:
                return Employee.objects.get(is_active=True, vat_number=employee.vat_number,
                                                          employee_type=LegacyEmployeeType.REGULAR)
            except Employee.DoesNotExist:
                pass

        # first with employee registry
        if employee.registry_id is not None:

            employee_registry_id = employee.registry_id

            if len(employee_registry_id.strip()) == 0:
                employee_registry_id = None
        else:
            employee_registry_id = None

        if employee_registry_id is not None:
            try:
                return Employee.objects.get(is_active=True, registry_id=employee_registry_id,
                                                          employee_type=LegacyEmployeeType.REGULAR)
            except Employee.DoesNotExist:
                pass

        return None

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        employee_afm = options['employee_afm']

        # find ADMINISTRATIVE employees
        employee_criteria = {
            'employee_type': LegacyEmployeeType.ADMINISTRATIVE,
            'is_active': True
        }

        if employee_afm is not None:
            employee_criteria['vat_number'] = employee_afm

        employees = Employee.objects.filter(**employee_criteria).order_by("last_name")

        self.stdout.write(
            self.style.SUCCESS(f'Found totally {employees.count()} ADMINISTRATIVE employees')
        )

        for employee in employees:

            # let's find a merge candidate
            self.stdout.write(
                self.style.SUCCESS(f'Handling {employee.vat_number} "{employee}"')
            )

            duplicate_employee: Employee = self.find_merge_candidate(employee)

            if duplicate_employee is None:
                self.stdout.write(
                    self.style.ERROR(f'!!! No candidate for {employee.vat_number} "{employee}"')
                )
                continue

            # we found a candidate for merging
            self.stdout.write(
                self.style.SUCCESS(f'[*] Found candidate {duplicate_employee.vat_number} "{duplicate_employee}"')
            )

            leaves_to_transfer = Leave.objects.filter(employee=duplicate_employee).order_by('-date_from')
            for leave in leaves_to_transfer:

                self.stdout.write(
                    self.style.SUCCESS(f'\t[+] migrating leave "{leave}"')
                )
                original_leave: Leave = Leave.objects.get(pk=leave.pk)

                if dry_run is False:
                    leave.pk = None
                    leave._state.adding = True
                    leave.original_leave = original_leave
                    if original_leave.leave_type.legacy_code == '54':
                        leave.leave_type = LeaveType.objects.get(legacy_code='54',
                                                                 suitable_for_employee_type=LegacyEmployeeType.ADMINISTRATIVE)
                    leave.employee = employee
                    leave.save()

            if dry_run is False:
                duplicate_employee.is_active = False
                duplicate_employee.save()









        # for employee in employees:
        #     print("**** deleting ", employee)
        #     if do_delete:
        #         employee.delete()
        # self.stdout.write(
        #     self.style.SUCCESS('Successfully deleted all employments')
        # )

        #
        #
        #
        #
        # if employee_type == LegacyEmployeeType.REGULAR:
        #     raise CommandError('Not allowed to remove regular employees')


        # for employee in employees:
        #     print("**** deleting ", employee)
        #     if do_delete:
        #         employee.delete()
        # self.stdout.write(
        #     self.style.SUCCESS('Successfully deleted all employments')
        # )