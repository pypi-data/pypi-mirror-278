from hestia_earth.schema import SchemaType
from hestia_earth.utils.api import download_hestia
from hestia_earth.utils.model import linked_node
from hestia_earth.utils.lookup import get_table_value, download_lookup, column_name

from . import _term_id, _include_methodModel
from .blank_node import find_terms_value
from .constant import Units, get_atomic_conversion


def _new_emission(term, model=None):
    node = {'@type': SchemaType.EMISSION.value}
    node['term'] = linked_node(term if isinstance(term, dict) else download_hestia(_term_id(term)))
    return _include_methodModel(node, model)


def is_in_system_boundary(term_id: str):
    lookup = download_lookup('emission.csv')
    value = get_table_value(lookup, 'termid', term_id, column_name('inHestiaDefaultSystemBoundary'))
    # handle numpy boolean
    return not (not value)


def get_nh3_no3_nox_to_n(cycle: dict, nh3_term_id: str, no3_term_id: str, nox_term_id: str, allow_none: bool = False):
    default_value = 0 if allow_none else None

    nh3 = find_terms_value(cycle.get('emissions', []), nh3_term_id, default=default_value)
    nh3 = None if nh3 is None else nh3 / get_atomic_conversion(Units.KG_NH3, Units.TO_N)
    no3 = find_terms_value(cycle.get('emissions', []), no3_term_id, default=default_value)
    no3 = None if no3 is None else no3 / get_atomic_conversion(Units.KG_NO3, Units.TO_N)
    nox = find_terms_value(cycle.get('emissions', []), nox_term_id, default=default_value)
    nox = None if nox is None else nox / get_atomic_conversion(Units.KG_NOX, Units.TO_N)

    return (nh3, no3, nox)
