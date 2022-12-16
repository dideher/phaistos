import uuid
from django.db import models


class BaseUUIDModel(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, null=False, editable=False)

    class Meta:
        abstract = True
