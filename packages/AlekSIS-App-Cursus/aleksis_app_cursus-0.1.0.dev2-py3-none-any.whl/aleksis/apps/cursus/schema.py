from django.core.exceptions import PermissionDenied
from django.db.models import Q

import graphene
from graphene_django.types import DjangoObjectType
from graphene_django_cud.mutations import (
    DjangoBatchCreateMutation,
    DjangoBatchDeleteMutation,
    DjangoBatchPatchMutation,
)
from guardian.shortcuts import get_objects_for_user

from aleksis.core.models import Group, Person
from aleksis.core.schema.base import (
    DjangoFilterMixin,
    FilterOrderList,
    PermissionBatchDeleteMixin,
    PermissionBatchPatchMixin,
    PermissionsTypeMixin,
)
from aleksis.core.schema.group import GroupType as GraphQLGroupType
from aleksis.core.schema.group_type import GroupTypeType
from aleksis.core.schema.person import PersonType as GraphQLPersonType
from aleksis.core.util.core_helpers import get_site_preferences, has_person

from .models import Course, Subject


class SubjectType(PermissionsTypeMixin, DjangoFilterMixin, DjangoObjectType):
    class Meta:
        model = Subject
        fields = (
            "id",
            "short_name",
            "name",
            "parent",
            "colour_fg",
            "colour_bg",
            "courses",
            "teachers",
        )
        filter_fields = {
            "id": ["exact"],
            "short_name": ["exact", "icontains"],
            "name": ["exact", "icontains"],
            "parent": ["exact", "in"],
            "colour_fg": ["exact"],
            "colour_bg": ["exact"],
            "courses": ["exact", "in"],
            "teachers": ["exact", "in"],
        }

    @classmethod
    def get_queryset(cls, queryset, info):
        if not info.context.user.has_perm("cursus.view_subject_rule"):
            raise PermissionDenied()
        return queryset

    @staticmethod
    def resolve_courses(root, info, **kwargs):
        return get_objects_for_user(info.context.user, "cursus.view_course", root.courses.all())


class SubjectBatchCreateMutation(DjangoBatchCreateMutation):
    class Meta:
        model = Subject
        permissions = ("cursus.create_subject_rule",)
        only_fields = (
            "short_name",
            "name",
            "parent",
            "colour_fg",
            "colour_bg",
            "courses",
            "teachers",
        )


class SubjectBatchDeleteMutation(PermissionBatchDeleteMixin, DjangoBatchDeleteMutation):
    class Meta:
        model = Subject
        permissions = ("cursus.delete_subject_rule",)


class SubjectBatchPatchMutation(PermissionBatchPatchMixin, DjangoBatchPatchMutation):
    class Meta:
        model = Subject
        permissions = ("cursus.edit_subject_rule",)
        only_fields = (
            "id",
            "short_name",
            "name",
            "parent",
            "colour_fg",
            "colour_bg",
            "courses",
            "teachers",
        )


class CourseInterface(graphene.Interface):
    id = graphene.ID()  # noqa: A003
    course_id = graphene.ID()
    name = graphene.String()
    subject = graphene.Field(SubjectType)
    teachers = graphene.List(GraphQLPersonType)
    groups = graphene.List(GraphQLGroupType)
    lesson_quota = graphene.Int()


class CourseType(PermissionsTypeMixin, DjangoFilterMixin, DjangoObjectType):
    class Meta:
        model = Course
        interfaces = (CourseInterface,)
        fields = ("id", "name", "subject", "teachers", "groups", "lesson_quota")
        filter_fields = {
            "id": ["exact"],
            "name": ["exact", "icontains"],
            "subject": ["exact", "in"],
            "subject__name": ["icontains"],
            "subject__short_name": ["icontains"],
            "teachers": ["in"],
            "groups": ["in"],
        }

    @staticmethod
    def resolve_teachers(root, info, **kwargs):
        if not info.context.user.has_perm("cursus.view_course_details_rule", root):
            raise PermissionDenied()
        teachers = get_objects_for_user(info.context.user, "core.view_person", root.teachers.all())

        # Fixme: this following code was copied from aleksis/core/schema/group.py so it should work
        #        It does however fail with the message "'Person' object has no attribute 'query'"
        # if has_person(info.context.user) and [
        #     m for m in root.teachers.all() if m.pk == info.context.user.person.pk
        # ]:
        #     teachers = (teachers | Person.objects.get(pk=info.context.user.person.pk)).distinct()
        return teachers

    @staticmethod
    def resolve_groups(root, info, **kwargs):
        if not info.context.user.has_perm("cursus.view_course_details_rule", root):
            raise PermissionDenied()
        by_permission = get_objects_for_user(
            info.context.user, "core.view_group", root.groups.all()
        )
        by_ownership = info.context.user.person.owner_of.all() & root.groups.all()
        return by_permission | by_ownership

    @staticmethod
    def resolve_course_id(root, info, **kwargs):
        return root.id

    @classmethod
    def get_queryset(cls, queryset, info):
        if not info.context.user.has_perm("cursus.view_course_rule"):
            raise PermissionDenied()
        return queryset


class TeacherType(GraphQLPersonType):
    class Meta:
        model = Person

    subjects_as_teacher = graphene.List(SubjectType)
    courses_as_teacher = graphene.List(CourseType)

    @staticmethod
    def resolve_subjects_as_teacher(root, info, **kwargs):
        return root.subjects_as_teacher.all()

    @staticmethod
    def resolve_courses_as_teacher(root, info, **kwargs):
        return root.courses_as_teacher.all()


class CourseBatchCreateMutation(DjangoBatchCreateMutation):
    class Meta:
        model = Course
        permissions = ("cursus.create_course_rule",)
        only_fields = ("name", "subject", "teachers", "groups", "lesson_quota")


class CourseBatchDeleteMutation(PermissionBatchDeleteMixin, DjangoBatchDeleteMutation):
    class Meta:
        model = Course
        permissions = ("cursus.delete_course_rule",)


class CourseBatchPatchMutation(PermissionBatchPatchMixin, DjangoBatchPatchMutation):
    class Meta:
        model = Course
        permissions = ("cursus.edit_course.rule",)
        only_fields = ("id", "name", "subject", "teachers", "groups", "lesson_quota")


class CreateSchoolStructureSecondLevelGroupsMutation(DjangoBatchCreateMutation):
    class Meta:
        model = Group
        permissions = ("core.add_group",)
        only_fields = ("name", "short_name", "school_term", "parent_groups")

    @classmethod
    def before_mutate(cls, root, info, input):  # noqa
        group_type = get_site_preferences()["cursus__school_structure_second_level_group_type"]
        if not group_type:
            raise PermissionDenied()
        for group in input:
            group["group_type"] = group_type.pk
        return input


class CreateSchoolStructureFirstLevelGroupsMutation(DjangoBatchCreateMutation):
    class Meta:
        model = Group
        permissions = ("core.add_group",)
        only_fields = ("name", "short_name", "school_term", "parent_groups")

    @classmethod
    def before_mutate(cls, root, info, input):  # noqa
        group_type = get_site_preferences()["cursus__school_structure_first_level_group_type"]
        if not group_type:
            raise PermissionDenied()
        for group in input:
            group["group_type"] = group_type.pk
        return input


class SchoolStructureQuery(graphene.ObjectType):
    first_level_type = graphene.Field(GroupTypeType)
    second_level_type = graphene.Field(GroupTypeType)
    first_level_groups = FilterOrderList(GraphQLGroupType)
    second_level_groups = FilterOrderList(GraphQLGroupType)
    first_level_groups_by_term = FilterOrderList(GraphQLGroupType, school_term=graphene.ID())

    @staticmethod
    def resolve_first_level_type(root, info, **kwargs):
        return get_site_preferences()["cursus__school_structure_first_level_group_type"]

    @staticmethod
    def resolve_second_level_type(root, info, **kwargs):
        return get_site_preferences()["cursus__school_structure_second_level_group_type"]

    @staticmethod
    def resolve_first_level_groups(root, info, **kwargs):
        group_type = get_site_preferences()["cursus__school_structure_first_level_group_type"]
        if not group_type:
            return []
        return get_objects_for_user(
            info.context.user,
            "core.view_group",
            Group.objects.filter(group_type=group_type),
        )

    @staticmethod
    def resolve_second_level_groups(root, info, **kwargs):
        group_type = get_site_preferences()["cursus__school_structure_second_level_group_type"]
        if not group_type:
            return []
        return get_objects_for_user(
            info.context.user,
            "core.view_group",
            Group.objects.filter(group_type=group_type),
        )

    @staticmethod
    def resolve_first_level_groups_by_term(root, info, school_term):
        group_type = get_site_preferences()["cursus__school_structure_first_level_group_type"]
        print(
            group_type,
            Group.objects.filter(school_term=school_term).filter(group_type=group_type),
        )
        if not group_type:
            return []
        return get_objects_for_user(
            info.context.user,
            "core.view_group",
            Group.objects.filter(school_term=school_term).filter(group_type=group_type),
        )


class Query(graphene.ObjectType):
    subjects = FilterOrderList(SubjectType)
    courses = FilterOrderList(CourseType)

    school_structure = graphene.Field(SchoolStructureQuery)

    teachers = FilterOrderList(TeacherType)

    course_by_id = graphene.Field(CourseType, id=graphene.ID())
    courses_of_teacher = FilterOrderList(CourseType, teacher=graphene.ID())

    def resolve_course_by_id(root, info, id):  # noqa
        course = Course.objects.get(pk=id)
        if not info.context.user.has_perm("cursus.view_course_rule", course):
            raise PermissionDenied()
        return course

    @staticmethod
    def resolve_teachers(root, info):
        return get_objects_for_user(
            info.context.user,
            "core.view_person",
            Person.objects.filter(
                Q(courses_as_teacher__isnull=False) | Q(subjects_as_teacher__isnull=False)
            ),
        )

    @staticmethod
    def resolve_courses_of_teacher(root, info, teacher=None):
        if not has_person(info.context.user):
            raise PermissionDenied()
        teacher = Person.objects.get(pk=teacher) if teacher else info.context.user.person
        # FIXME: Permission checking. But maybe it's done in get_queryset
        return teacher.courses_as_teacher.all()

    @staticmethod
    def resolve_school_structure(root, info):
        return True


class Mutation(graphene.ObjectType):
    create_subjects = SubjectBatchCreateMutation.Field()
    delete_subjects = SubjectBatchDeleteMutation.Field()
    update_subjects = SubjectBatchPatchMutation.Field()

    create_courses = CourseBatchCreateMutation.Field()
    delete_courses = CourseBatchDeleteMutation.Field()
    update_courses = CourseBatchPatchMutation.Field()

    create_first_level_groups = CreateSchoolStructureFirstLevelGroupsMutation.Field()
    create_second_level_groups = CreateSchoolStructureSecondLevelGroupsMutation.Field()
