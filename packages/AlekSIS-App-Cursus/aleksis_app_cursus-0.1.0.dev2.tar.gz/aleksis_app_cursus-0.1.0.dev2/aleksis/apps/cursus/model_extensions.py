from django.apps import apps
from django.db.models import Model
from django.utils.translation import gettext as _

from .models import Course, Subject

if apps.is_installed("aleksis.apps.csv_import"):
    from aleksis.apps.csv_import.field_types import ProcessFieldType

    class GroupSubjectByShortNameFieldType(ProcessFieldType):
        name = "group_subject_short_name"
        verbose_name = _("Short name of the subject")

        def process(self, instance: Model, value):
            subject, __ = Subject.objects.get_or_create(short_name=value, defaults={"name": value})
            instance.subject = subject
            instance.save()

    class SubjectByShortNameFieldType(ProcessFieldType):
        name = "subject_by_short_name"
        verbose_name = _("Short name of the subject")
        run_before_save = True

        def process(self, instance: Model, value):
            subject, __ = Subject.objects.get_or_create(short_name=value, defaults={"name": value})
            instance.subject = subject

    class CourseByUniqueReferenceFieldType(ProcessFieldType):
        name = "course_by_unique_reference"
        verbose_name = _("Short name of the subject")
        run_before_save = True

        def process(self, instance: Model, value):
            course = Course.objects.get(extended_data__import_ref_csv=value)
            instance.course = course
