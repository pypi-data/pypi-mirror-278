from polymorphic.managers import PolymorphicQuerySet

from aleksis.core.managers import DateRangeQuerySetMixin
from aleksis.core.models import Person


class AbsenceQuerySet(DateRangeQuerySetMixin, PolymorphicQuerySet):
    """QuerySet with custom query methods for absences."""

    def absent_persons(self):
        return Person.objects.filter(absences__in=self).distinct().order_by("short_name")
