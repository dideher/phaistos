from django.core.management.base import BaseCommand, CommandError
from employees.models import Employment

class Command(BaseCommand):

    def handle(self, *args, **options):

        Employment.objects.all().delete()
        self.stdout.write(
            self.style.SUCCESS('Successfully deleted all employments')
        )
