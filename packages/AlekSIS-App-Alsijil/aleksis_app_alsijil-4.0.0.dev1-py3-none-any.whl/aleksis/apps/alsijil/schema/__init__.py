from datetime import datetime

from django.core.exceptions import PermissionDenied
from django.db.models.query_utils import Q

import graphene

from aleksis.apps.chronos.models import LessonEvent
from aleksis.apps.cursus.models import Course
from aleksis.apps.cursus.schema import CourseType
from aleksis.core.models import Group, Person
from aleksis.core.schema.base import FilterOrderList
from aleksis.core.schema.group import GroupType
from aleksis.core.util.core_helpers import has_person

from ..models import Documentation
from .documentation import (
    DocumentationBatchCreateOrUpdateMutation,
    DocumentationType,
    LessonsForPersonType,
    TouchDocumentationMutation,
)
from .participation_status import ParticipationStatusBatchPatchMutation


class Query(graphene.ObjectType):
    documentations = FilterOrderList(DocumentationType)
    documentations_by_course_id = FilterOrderList(
        DocumentationType, course_id=graphene.ID(required=True)
    )
    documentations_for_coursebook = FilterOrderList(
        DocumentationType,
        own=graphene.Boolean(required=True),
        obj_type=graphene.String(required=False),
        obj_id=graphene.ID(required=False),
        date_start=graphene.Date(required=True),
        date_end=graphene.Date(required=True),
        incomplete=graphene.Boolean(required=False),
    )

    groups_by_person = FilterOrderList(GroupType, person=graphene.ID())
    courses_of_person = FilterOrderList(CourseType, person=graphene.ID())

    lessons_for_persons = graphene.List(
        LessonsForPersonType,
        persons=graphene.List(graphene.ID, required=True),
        start=graphene.Date(required=True),
        end=graphene.Date(required=True),
    )

    def resolve_documentations_by_course_id(root, info, course_id, **kwargs):
        documentations = Documentation.objects.filter(
            Q(course__pk=course_id) | Q(amends__course__pk=course_id)
        )
        return documentations

    def resolve_documentations_for_coursebook(
        root,
        info,
        own,
        date_start,
        date_end,
        obj_type=None,
        obj_id=None,
        incomplete=False,
        **kwargs,
    ):
        if (
            (
                obj_type == "COURSE"
                and not info.context.user.has_perm(
                    "alsijil.view_documentations_for_course_rule", Course.objects.get(id=obj_id)
                )
            )
            or (
                obj_type == "GROUP"
                and not info.context.user.has_perm(
                    "alsijil.view_documentations_for_group_rule", Group.objects.get(id=obj_id)
                )
            )
            or (
                obj_type == "TEACHER"
                and not info.context.user.has_perm(
                    "alsijil.view_documentations_for_teacher_rule", Person.objects.get(id=obj_id)
                )
            )
        ):
            raise PermissionDenied()

        # Find all LessonEvents for all Lessons of this Course in this date range
        event_params = {
            "own": own,
        }
        if obj_type is not None and obj_id is not None:
            event_params.update(
                {
                    "type": obj_type,
                    "id": obj_id,
                }
            )

        events = LessonEvent.get_single_events(
            datetime.combine(date_start, datetime.min.time()),
            datetime.combine(date_end, datetime.max.time()),
            info.context,
            event_params,
            with_reference_object=True,
        )

        # Lookup or create documentations and return them all.
        docs, dummies = Documentation.get_documentations_for_events(events, incomplete)
        return docs + dummies

    @staticmethod
    def resolve_groups_by_person(root, info, person=None):
        if person:
            person = Person.objects.get(pk=person)
            if not info.context.user.has_perm("core.view_person_rule", person):
                raise PermissionDenied()
        elif has_person(info.context.user):
            person = info.context.user.person
        else:
            raise PermissionDenied()

        return Group.objects.filter(
            Q(members=person) | Q(owners=person) | Q(parent_groups__owners=person)
        )

    @staticmethod
    def resolve_courses_of_person(root, info, person=None):
        if person:
            person = Person.objects.get(pk=person)
            if not info.context.user.has_perm("core.view_person_rule", person):
                raise PermissionDenied()
        elif has_person(info.context.user):
            person = info.context.user.person
        else:
            raise PermissionDenied()

        return Course.objects.filter(
            Q(teachers=person)
            | Q(groups__members=person)
            | Q(groups__owners=person)
            | Q(groups__parent_groups__owners=person)
        )

    @staticmethod
    def resolve_lessons_for_persons(
        root,
        info,
        persons,
        start,
        end,
        **kwargs,
    ):
        """Resolve all lesson events for each person in timeframe start to end."""
        lessons_for_person = []
        for person in persons:
            docs, dummies = Documentation.get_documentations_for_person(
                person,
                datetime.combine(start, datetime.min.time()),
                datetime.combine(end, datetime.max.time()),
            )

            lessons_for_person.append(id=person, lessons=docs + dummies)

        return lessons_for_person


class Mutation(graphene.ObjectType):
    create_or_update_documentations = DocumentationBatchCreateOrUpdateMutation.Field()
    touch_documentation = TouchDocumentationMutation.Field()
    update_participation_statuses = ParticipationStatusBatchPatchMutation.Field()
