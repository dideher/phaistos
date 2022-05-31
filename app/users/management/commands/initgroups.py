# inspired from https://www.devasking.com/issue/create-django-group
from django.core.management import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from leaves import models as leave_models
from employees import models as employee_model

GROUPS_PERMISSIONS = {
    'EmployeeViewer': {
        employee_model.Employee: ['view', ]
    },
    'LeaveViewer': {
        leave_models.Leave: ['view', ],
    },
    'LeaveManager': {
        leave_models.Leave: ['add', 'change', 'view'],
    },
    'LeaveAdmin': {
        leave_models.Leave: ['add', 'change', 'delete', 'view'],
    },
    'LeaveReporting': {
        leave_models.Leave: ['search', 'export'],
    }
}


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    help = "Create default groups"

    def handle(self, *args, **options):
        # Loop groups
        for group_name in GROUPS_PERMISSIONS:

            # Get or create group
            group, created = Group.objects.get_or_create(name=group_name)

            # Loop models in group
            for model_cls in GROUPS_PERMISSIONS[group_name]:
                # Loop permissions in group/model
                for perm_index, perm_name in \
                        enumerate(GROUPS_PERMISSIONS[group_name][model_cls]):

                    # Generate permission name as Django would generate it
                    codename = perm_name + "_" + model_cls._meta.model_name

                    try:
                        # Find permission object and add to group
                        perm = Permission.objects.get(codename=codename)
                    except Permission.DoesNotExist:
                        ct = ContentType.objects.get_for_model(model_cls)
                        perm = Permission.objects.create(codename=codename,
                                                         name='Can ' + codename,
                                                         content_type=ct)
                    group.permissions.add(perm)
                    self.stdout.write("Adding "
                                      + codename
                                      + " to group "
                                      + group.__str__())
