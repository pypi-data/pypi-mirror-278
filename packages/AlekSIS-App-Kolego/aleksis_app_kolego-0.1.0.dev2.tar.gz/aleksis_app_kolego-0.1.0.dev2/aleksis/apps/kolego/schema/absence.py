from datetime import timezone

from django.conf import settings

from graphene_django.types import DjangoObjectType
from guardian.shortcuts import get_objects_for_user
from zoneinfo import ZoneInfo

from aleksis.core.schema.base import (
    BaseBatchCreateMutation,
    BaseBatchDeleteMutation,
    BaseBatchPatchMutation,
    DjangoFilterMixin,
    PermissionsTypeMixin,
)

from ..models import Absence, AbsenceReason


class AbsenceReasonType(PermissionsTypeMixin, DjangoFilterMixin, DjangoObjectType):
    class Meta:
        model = AbsenceReason
        fields = ("id", "short_name", "name", "colour", "default")
        filter_fields = {
            "short_name": ["icontains", "exact"],
            "name": ["icontains", "exact"],
        }

    @classmethod
    def get_queryset(cls, queryset, info):
        if not info.context.user.has_perm("kolego.fetch_absencereasons_rule"):
            return []
        return queryset


class AbsenceType(PermissionsTypeMixin, DjangoFilterMixin, DjangoObjectType):
    class Meta:
        model = Absence
        fields = ("id", "person", "reason", "comment", "datetime_start", "datetime_end")
        filter_fields = {
            "person__full_name": ["icontains", "exact"],
            "comment": ["icontains", "exact"],
        }

    @classmethod
    def get_queryset(cls, queryset, info):
        return get_objects_for_user(info.context.user, "kolego.view_absence", queryset)


class AbsenceBatchCreateMutation(BaseBatchCreateMutation):
    class Meta:
        model = Absence
        fields = ("person", "reason", "comment", "datetime_start", "datetime_end")
        optional_fields = ("comment", "reason")
        permissions = ("kolego.create_absence_rule",)

    @classmethod
    def handle_datetime_start(cls, value, name, info) -> int:
        value = value.replace(tzinfo=timezone.utc)
        return value

    @classmethod
    def handle_datetime_end(cls, value, name, info) -> int:
        value = value.replace(tzinfo=timezone.utc)
        return value

    @classmethod
    def before_save(cls, root, info, input, obj):  # noqa: A002
        for absence in obj:
            absence.timezone = ZoneInfo(settings.TIME_ZONE)  # FIXME Use TZ provided by client
        return obj


class AbsenceBatchDeleteMutation(BaseBatchDeleteMutation):
    class Meta:
        model = Absence
        permissions = ("kolego.delete_absence_rule",)


class AbsenceBatchPatchMutation(BaseBatchPatchMutation):
    class Meta:
        model = Absence
        fields = ("id", "person", "reason", "comment", "datetime_start", "datetime_end")
        permissions = ("kolego.edit_absence_rule",)

    @classmethod
    def handle_datetime_start(cls, value, name, info) -> int:
        value = value.replace(tzinfo=timezone.utc)
        return value

    @classmethod
    def handle_datetime_end(cls, value, name, info) -> int:
        value = value.replace(tzinfo=timezone.utc)
        return value

    @classmethod
    def before_save(cls, root, info, input, obj):  # noqa: A002
        for absence in obj:
            absence.timezone = ZoneInfo(settings.TIME_ZONE)  # FIXME Use TZ provided by client
        return obj


class AbsenceReasonBatchCreateMutation(BaseBatchCreateMutation):
    class Meta:
        model = AbsenceReason
        fields = ("short_name", "name", "colour", "default")
        optional_fields = ("name",)
        permissions = ("kolego.create_absencereason_rule",)


class AbsenceReasonBatchDeleteMutation(BaseBatchDeleteMutation):
    class Meta:
        model = AbsenceReason
        permissions = ("kolego.delete_absencereason_rule",)


class AbsenceReasonBatchPatchMutation(BaseBatchPatchMutation):
    class Meta:
        model = AbsenceReason
        fields = ("id", "short_name", "name", "colour", "default")
        permissions = ("kolego.edit_absencereason_rule",)
