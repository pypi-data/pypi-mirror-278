import rules

from aleksis.apps.kolego.models.absence import Absence, AbsenceReason
from aleksis.core.util.predicates import (
    has_any_object,
    has_global_perm,
    has_object_perm,
    has_person,
)

view_absences_predicate = has_person & (
    has_global_perm("kolego.view_absence") | has_any_object("kolego.view_absence", Absence)
)
rules.add_perm("kolego.view_absences_rule", view_absences_predicate)

view_absence_predicate = has_person & (
    has_global_perm("kolego.view_absence") | has_object_perm("kolego.view_absence")
)
rules.add_perm("kolego.view_absence_rule", view_absence_predicate)

create_absence_predicate = has_person & (has_global_perm("kolego.add_absence"))
rules.add_perm("kolego.create_absence_rule", create_absence_predicate)

edit_absence_predicate = has_person & (
    has_global_perm("kolego.change_absence") | has_object_perm("kolego.change_absence")
)
rules.add_perm("kolego.edit_absence_rule", edit_absence_predicate)

delete_absence_predicate = has_person & (
    has_global_perm("kolego.delete_absence") | has_object_perm("kolego.delete_absence")
)
rules.add_perm("kolego.delete_absence_rule", delete_absence_predicate)

fetch_absencereasons_predicate = has_person
rules.add_perm("kolego.fetch_absencereasons_rule", fetch_absencereasons_predicate)

view_absencereasons_predicate = has_person & (
    has_global_perm("kolego.view_absencereason")
    | has_any_object("kolego.view_absencereason", AbsenceReason)
)
rules.add_perm("kolego.view_absencereasons_rule", view_absencereasons_predicate)

view_absencereason_predicate = has_person & (
    has_global_perm("kolego.view_absencereason") | has_object_perm("kolego.view_absencereason")
)
rules.add_perm("kolego.view_absencereason_rule", view_absencereason_predicate)

create_absencereason_predicate = has_person & (has_global_perm("kolego.add_absencereason"))
rules.add_perm("kolego.create_absencereason_rule", create_absencereason_predicate)

edit_absencereason_predicate = has_person & (
    has_global_perm("kolego.change_absencereason") | has_object_perm("kolego.change_absencereason")
)
rules.add_perm("kolego.edit_absencereason_rule", edit_absencereason_predicate)

delete_absencereason_predicate = has_person & (
    has_global_perm("kolego.delete_absencereason") | has_object_perm("kolego.delete_absencereason")
)
rules.add_perm("kolego.delete_absencereason_rule", delete_absencereason_predicate)

view_menu_predicate = has_person & (view_absences_predicate | view_absencereasons_predicate)
rules.add_perm("kolego.view_menu_rule", view_menu_predicate)
