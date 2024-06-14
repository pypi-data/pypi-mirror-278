from django.core.exceptions import PermissionDenied

from graphene_django import DjangoObjectType

from aleksis.apps.alsijil.models import ParticipationStatus
from aleksis.core.schema.base import (
    BaseBatchPatchMutation,
    DjangoFilterMixin,
    OptimisticResponseTypeMixin,
    PermissionsTypeMixin,
)


class ParticipationStatusType(
    OptimisticResponseTypeMixin,
    PermissionsTypeMixin,
    DjangoFilterMixin,
    DjangoObjectType,
):
    class Meta:
        model = ParticipationStatus
        fields = (
            "id",
            "person",
            "absence_reason",
            "related_documentation",
            "base_absence",
        )


class ParticipationStatusBatchPatchMutation(BaseBatchPatchMutation):
    class Meta:
        model = ParticipationStatus
        fields = ("id", "absence_reason")  # Only the reason can be updated after creation
        return_field_name = "participationStatuses"

    @classmethod
    def check_permissions(cls, root, info, input, *args, **kwargs):  # noqa: A002
        pass

    @classmethod
    def after_update_obj(cls, root, info, input, obj, full_input):  # noqa: A002
        if not info.context.user.has_perm(
            "alsijil.edit_participation_status_for_documentation_rule", obj.related_documentation
        ):
            raise PermissionDenied()
