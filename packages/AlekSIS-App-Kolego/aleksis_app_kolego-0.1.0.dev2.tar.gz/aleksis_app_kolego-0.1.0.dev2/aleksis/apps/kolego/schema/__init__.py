from django.apps import apps

import graphene

from aleksis.core.schema.base import FilterOrderList

from .absence import (
    AbsenceBatchCreateMutation,
    AbsenceBatchDeleteMutation,
    AbsenceBatchPatchMutation,
    AbsenceReasonBatchCreateMutation,
    AbsenceReasonBatchDeleteMutation,
    AbsenceReasonBatchPatchMutation,
    AbsenceReasonType,
    AbsenceType,
)


class Query(graphene.ObjectType):
    app_name = graphene.String()
    absences = FilterOrderList(AbsenceType)
    absence_reasons = FilterOrderList(AbsenceReasonType)

    def resolve_app_name(root, info, **kwargs) -> str:
        return apps.get_app_config("kolego").verbose_name


class Mutation(graphene.ObjectType):
    create_absences = AbsenceBatchCreateMutation.Field()
    delete_absences = AbsenceBatchDeleteMutation.Field()
    update_absences = AbsenceBatchPatchMutation.Field()

    create_absence_reasons = AbsenceReasonBatchCreateMutation.Field()
    delete_absence_reasons = AbsenceReasonBatchDeleteMutation.Field()
    update_absence_reasons = AbsenceReasonBatchPatchMutation.Field()
