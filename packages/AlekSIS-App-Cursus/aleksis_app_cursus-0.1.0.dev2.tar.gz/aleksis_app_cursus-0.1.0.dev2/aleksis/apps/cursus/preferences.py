from django.utils.translation import gettext_lazy as _

from dynamic_preferences.preferences import Section
from dynamic_preferences.types import ModelChoicePreference

from aleksis.core.models import GroupType
from aleksis.core.registries import site_preferences_registry

cursus = Section("cursus", verbose_name=_("Course management"))


@site_preferences_registry.register
class SchoolStructureFirstLevelGroupType(ModelChoicePreference):
    section = cursus
    name = "school_structure_first_level_group_type"
    required = False
    default = None
    model = GroupType
    verbose_name = _("School structure: Group type for first level (e. g. grades)")
    help_text = _(
        "You have to set this and the second level group type to use the school structure tool."
    )


@site_preferences_registry.register
class SchoolStructureSecondLevelGroupType(ModelChoicePreference):
    section = cursus
    name = "school_structure_second_level_group_type"
    required = False
    default = None
    model = GroupType
    verbose_name = _("School structure: Group type for second level (e. g. classes)")
    help_text = _(
        "You have to set this and the first level group type to use the school structure tool."
    )
