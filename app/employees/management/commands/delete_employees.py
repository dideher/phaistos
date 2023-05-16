from django.core.management.base import BaseCommand, CommandError
from employees.models import Employment, LegacyEmployeeType, Employee

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument("employee_type", type=str)

        parser.add_argument(
            "--delete",
            action="store_true",
            help="actually delete duplicate employee",
        )

    def handle(self, *args, **options):
        employee_type_str = options['employee_type']
        employee_type = LegacyEmployeeType[employee_type_str]
        do_delete = options['delete']
        if employee_type == LegacyEmployeeType.REGULAR:
            raise CommandError('Not allowed to remove regular employees')

        employees = Employee.objects.filter(employee_type=employee_type)
        for employee in employees:
            print("**** deleting ", employee)
            if do_delete:
                employee.delete()
        self.stdout.write(
            self.style.SUCCESS('Successfully deleted all employments')
        )
