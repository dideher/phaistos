from django.core.management.base import BaseCommand, CommandError
from leaves.models import Leave, LeaveType


class Command(BaseCommand):

    def add_arguments(self, parser):

        parser.add_argument(
            "--employee_afm",
            type=str,
            help="employee AFM",
        )

    def handle(self, *args, **options):
        employee_afm = options['employee_afm']

        filters = {
            'is_deleted': False,
            'leave_type__count_against_teaching_experience': True
        }

        if employee_afm is not None:
            filters.update({
                'employee__vat_number': employee_afm
            })

        leaves_updated_with_true = Leave.objects.filter(**filters).update(count_against_teaching_experience=True)

        # now, do the opposite for the rest of the leaves
        filters['leave_type__count_against_teaching_experience'] = False
        leaves_updated_with_false = Leave.objects.filter(**filters).update(count_against_teaching_experience=False)

        self.stdout.write(
            self.style.SUCCESS(f'updated {leaves_updated_with_true} leave(s) with count_against_teaching_experience '
                               f'set to true')
        )

        self.stdout.write(
            self.style.SUCCESS(
                f'updated {leaves_updated_with_false} leave(s) with count_against_teaching_experience set to false')
        )