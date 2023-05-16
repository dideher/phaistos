from django.core.management.base import BaseCommand, CommandError
from employees.models import Employment, LegacyEmployeeType, Employee

class Command(BaseCommand):

    def add_arguments(self, parser):

        parser.add_argument(
            "--delete",
            action="store_true",
            help="actually delete duplicate employee",
        )

    def handle(self, *args, **options):

        #employee_type_str = options['employee_type']
        employee_type_str = 'DEPUTY'

        Employment.objects.all().delete()
        self.stdout.write(
            self.style.SUCCESS('Successfully deleted all employments')
        )
