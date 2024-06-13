from django.db import models
from django.db.models import QuerySet
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _

from colorfield.fields import ColorField

from aleksis.core.managers import PolymorphicBaseManager
from aleksis.core.mixins import ExtensibleModel
from aleksis.core.models import FreeBusy

from ..managers import AbsenceQuerySet


class AbsenceReason(ExtensibleModel):
    short_name = models.CharField(verbose_name=_("Short name"), max_length=255, unique=True)
    name = models.CharField(verbose_name=_("Name"), max_length=255)

    colour = ColorField(verbose_name=_("Colour"), blank=True)

    count_as_absent = models.BooleanField(
        default=True,
        verbose_name=_("Count as absent"),
        help_text=_(
            "If checked, this excuse type will be counted as absent. If not checked,"
            "it won't show up in absence reports."
        ),
    )

    default = models.BooleanField(verbose_name=_("Default Reason"), default=False)

    def __str__(self):
        if self.name:
            return f"{self.short_name} ({self.name})"
        else:
            return self.short_name

    def save(self, *args, **kwargs):
        # Ensure that there is only one default absence reason
        if self.default:
            reasons = AbsenceReason.objects.filter(default=True)
            if self.pk:
                reasons.exclude(pk=self.pk)
            reasons.update(default=False)
        super().save(*args, **kwargs)

    @classmethod
    def get_default(cls) -> "AbsenceReason":
        try:
            return cls.objects.get(default=True)
        except cls.ObjectDoesNotExist:
            return cls.objects.create(default=True, short_name="u", name=_("Unexcused"))

    @property
    def count_label(self):
        return f"reason_{self.id}_count"

    class Meta:
        verbose_name = _("Absence reason")
        verbose_name_plural = _("Absence reasons")
        constraints = [
            models.UniqueConstraint(
                fields=["default"],
                condition=models.Q(default=True),
                name="only_one_default_absence_reason",
            )
        ]


class Absence(FreeBusy):
    objects = PolymorphicBaseManager.from_queryset(AbsenceQuerySet)()

    reason = models.ForeignKey(
        "AbsenceReason",
        on_delete=models.PROTECT,
        related_name="absences",
        verbose_name=_("Absence reason"),
    )

    person = models.ForeignKey(
        "core.Person",
        on_delete=models.CASCADE,
        related_name="kolego_absences",
        verbose_name=_("Person"),
    )

    comment = models.TextField(verbose_name=_("Comment"), blank=True)

    @classmethod
    def get_objects(
        cls, request: HttpRequest | None = None, params: dict[str, any] | None = None
    ) -> QuerySet:
        qs = super().get_objects(request, params).select_related("person", "reason")
        if params:
            if params.get("person"):
                qs = qs.filter(person_id=params["person"])
            elif params.get("persons"):
                qs = qs.filter(person_id__in=params["persons"])
            elif params.get("group"):
                qs = qs.filter(person__member_of__id=params.get("group"))
        return qs

    @classmethod
    def value_title(cls, reference_object: "Absence", request: HttpRequest | None = None) -> str:
        """Return the title of the calendar event."""
        return f"{reference_object.person} ({reference_object.reason})"

    @classmethod
    def value_description(
        cls, reference_object: "Absence", request: HttpRequest | None = None
    ) -> str:
        """Return the title of the calendar event."""
        return ""

    def __str__(self):
        return f"{self.person} ({self.datetime_start} - {self.datetime_end})"

    class Meta:
        verbose_name = _("Absence")
        verbose_name_plural = _("Absences")
