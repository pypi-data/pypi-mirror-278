from django.utils.translation import gettext_lazy as _

from dynamic_preferences.preferences import Section
from dynamic_preferences.types import BooleanPreference, ModelChoicePreference

from aleksis.core.models import GroupType
from aleksis.core.registries import site_preferences_registry

lesrooster = Section("lesrooster", verbose_name=_("Lesson management"))


@site_preferences_registry.register
class UseParentGroups(BooleanPreference):
    section = lesrooster
    name = "create_course_group"
    default = False
    verbose_name = _("Create course group when planning new courses")
    help_text = _(
        "If creating a new course with the 'Plan courses'"
        " feature, also create a seperate course group"
        " with the original group(s) as parent group(s) and"
        " link that/these group(s) to the newly created course"
    )


@site_preferences_registry.register
class GroupTypeCourseGroups(ModelChoicePreference):
    section = lesrooster
    name = "group_type_course_groups"
    required = False
    default = None
    model = GroupType
    verbose_name = _("Group type for automatically created course groups")
    help_text = _("If you leave it empty, no group type will be used.")

    def get_queryset(self):
        return GroupType.objects.managed_and_unmanaged()


@site_preferences_registry.register
class FillCourseGroupsWithMembers(BooleanPreference):
    section = lesrooster
    name = "fill_course_groups_with_members"
    default = True
    verbose_name = _("Fill course group with the given courses' members")
    help_text = _(
        "If creating a new course with the 'Plan courses'"
        " feature, fill the seperately created course group"
        " with the members of the original group(s)."
    )
