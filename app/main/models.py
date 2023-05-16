from __future__ import annotations

import uuid

from typing import Union
from django.db import models
from datetime import date

from django.db.models import DateField


class SingleActiveModelMixin(models.Model):

    is_active = models.BooleanField(db_column="IS_ACTIVE", default=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.is_active is True:
            # select all other active items
            qs = type(self).objects.filter(is_active=True)
            # except self (if self already exists)
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            # and deactive them
            qs.update(is_active=False)

        super().save(*args, **kwargs)


class BaseUUIDModel(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, null=False, editable=False)

    class Meta:
        abstract = True


class SchoolYear(SingleActiveModelMixin):
    """
    Models a School Year
    """
    year = models.PositiveIntegerField(db_column="YEAR", null=False, blank=False)
    date_from = models.DateField(db_column="DATE_FROM", null=False, blank=False)
    date_until = models.DateField(db_column="DATE_UNTIL", null=False, blank=False)

    # class Meta:
    #     indexes = [
    #         models.Index(fields=['year', ]),
    #     ]

    @staticmethod
    def get_current_school_year() -> Union[SchoolYear, None]:
        try:
            return SchoolYear.objects.get(is_active=True)
        except SchoolYear.DoesNotExist:
            return None

    @classmethod
    def get_or_create_school_year(cls, reference_date: date) -> SchoolYear:
        """
        Constructs or returns a school year based on a reference date
        :param reference_date:
        :return:
        """
        m = reference_date.month

        if m >= 9 <= 12:
            school_year = reference_date.year
        else:
            school_year = reference_date.year - 1

        try:
            return cls.objects.get(year=school_year)
        except cls.DoesNotExist:
            return cls.objects.create(
                year=school_year,
                date_from=date(day=1, month=9, year=school_year),
                date_until=date(day=30, month=6, year=school_year+1)
            )

    def __str__(self):
        return f'{self.date_from.year} - {self.date_until.year}'

