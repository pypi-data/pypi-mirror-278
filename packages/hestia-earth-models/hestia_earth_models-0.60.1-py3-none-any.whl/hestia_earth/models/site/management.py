"""
Management node with data gap-filled data from cycles.
"""
from typing import List, Any
from functools import reduce
from hestia_earth.schema import SchemaType, TermTermType
from hestia_earth.utils.api import download_hestia
from hestia_earth.utils.model import filter_list_term_type, linked_node
from hestia_earth.utils.tools import flatten, safe_parse_float

from hestia_earth.models.log import logRequirements, logShouldRun, log_blank_nodes_id
from hestia_earth.models.utils.term import get_lookup_value
from hestia_earth.models.utils.blank_node import get_node_value
from hestia_earth.models.utils.site import related_cycles
from . import MODEL

REQUIREMENTS = {
    "Site": {
        "related": {
            "Cycle": [{
                "@type": "Cycle",
                "startDate": "",
                "endDate": "",
                "products": [
                    {
                        "@type": "Product",
                        "term.termType": ["crop", "forage", "landCover"]
                    }
                ],
                "practices": [
                    {
                        "term.termType": [
                            "waterRegime",
                            "tillage",
                            "cropResidueManagement",
                            "landUseManagement"
                        ],
                        "value": ""
                    }
                ],
                "inputs": [
                    {
                        "@type": "Input",
                        "term.termType": [
                            "inorganicFertiliser",
                            "organicFertiliser",
                            "soilAmendment"
                        ]
                    }
                ]
            }]
        }
    }
}
RETURNS = {
    "Management": [{
        "@type": "Management",
        "term.termType": [
            "landCover", "waterRegime", "tillage", "cropResidueManagement", "landUseManagement"
        ],
        "value": "",
        "endDate": "",
        "startDate": ""
    }]
}
LOOKUPS = {
    "crop": ["landCoverTermId"],
    "forage": ["landCoverTermId"],
    "inorganicFertiliser": "nitrogenContent",
    "organicFertiliser": "ANIMAL_MANURE",
    "soilAmendment": "PRACTICE_INCREASING_C_INPUT"
}
MODEL_KEY = 'management'
LAND_COVER_KEY = LOOKUPS['crop'][0]
ANIMAL_MANURE_USED_TERM_ID = "animalManureUsed"
INORGANIC_NITROGEN_FERTILISER_USED_TERM_ID = "inorganicNitrogenFertiliserUsed"
ORGANIC_FERTILISER_USED_TERM_ID = "organicFertiliserUsed"
AMENDMENT_INCREASING_C_USED_TERM_ID = "amendmentIncreasingSoilCarbonUsed"
INPUT_RULES = {
    TermTermType.INORGANICFERTILISER.value: (
        (
            TermTermType.INORGANICFERTILISER.value,  # Lookup column
            lambda x: safe_parse_float(x) > 0,  # Condition
            INORGANIC_NITROGEN_FERTILISER_USED_TERM_ID  # New term.
        ),
    ),
    TermTermType.SOILAMENDMENT.value: (
        (
            TermTermType.SOILAMENDMENT.value,
            lambda x: x is True,
            AMENDMENT_INCREASING_C_USED_TERM_ID
        ),
    ),
    TermTermType.ORGANICFERTILISER.value: (
        (
            TermTermType.SOILAMENDMENT.value,
            lambda x: x is True,
            ORGANIC_FERTILISER_USED_TERM_ID
        ),
        (
            TermTermType.ORGANICFERTILISER.value,
            lambda x: x is True,
            ANIMAL_MANURE_USED_TERM_ID
        )
    )
}


def management(data: dict):
    node = {'@type': SchemaType.MANAGEMENT.value}
    return node | data


def _extract_node_value(node: dict) -> dict:
    return node | {'value': get_node_value(node)}


def _include(value: dict, keys: list): return {k: v for k, v in value.items() if k in keys}


def _include_start_end(cycle: dict, values: list):
    return [(_include(cycle, ['startDate', 'endDate']) | v) for v in values]


def _copy_item_if_exists(source: dict, keys: List[str] = None, dest: dict = None) -> dict:
    keys = keys or []
    dest = dest or {}
    return reduce(lambda p, c: p | ({c: source[c]} if c in source else {}), keys, dest)


def _get_landCover_term_id(product: dict) -> str:
    value = get_lookup_value(product.get('term', {}), LAND_COVER_KEY, model=MODEL, model_key=LAND_COVER_KEY)
    # TODO: what should happen when there are multiple values?
    return value.split(';')[0] if value else None


def _get_items_with_relevant_term_type(cycles: List[dict], item_name: str, relevant_values: list):
    """Get items from the list of cycles with any of the relevant values. Also adds dates if missing."""
    return flatten(
        [
            _include_start_end(
                cycle=cycle,
                values=filter_list_term_type(cycle.get(item_name, []), relevant_values)
            ) for cycle in cycles
        ]
    )


def _get_lookup_with_debug(term: dict, column: str) -> Any:
    get_lookup_value(term, column, model_key=MODEL_KEY, land_cover_key=LAND_COVER_KEY)


def _data_from_input(cycle: dict, term_id: str) -> dict:
    return {
        "term": {
            "@type": "Term",
            "@id": term_id,
            "termType": "landUseManagement"
        },
        "value": True,
        "startDate": cycle["startDate"],
        "endDate": cycle["endDate"]
    }


def _process_rule(cycle, term, term_type) -> List:
    relevant_terms = []
    for column, condition, new_term in INPUT_RULES[term_type]:
        lookup_result = _get_lookup_with_debug(term, LOOKUPS[column])

        if condition(lookup_result):
            relevant_terms.append(_data_from_input(cycle=cycle, term_id=new_term))

    return relevant_terms


def _get_relevant_inputs(cycles: List[dict]) -> List:
    relevant_inputs = []
    for cycle in [c for c in cycles if "inputs" in c]:
        for i in cycle["inputs"]:
            if i.get("term", {}).get("termType", "") in INPUT_RULES:
                relevant_inputs.extend(
                    _process_rule(
                        cycle=cycle,
                        term=i.get("term", {}),
                        term_type=i.get("term", {}).get("termType", "")
                    )
                )

    return relevant_inputs


def _should_run(site: dict):
    # Only get related cycles once.
    cycles = related_cycles(site.get("@id"))

    products_land_cover = [
        _extract_node_value(
            _include(
                value=product,
                keys=["term", "value", "startDate", "endDate", "properties"]
            )
        ) for product in _get_items_with_relevant_term_type(
            cycles=cycles,
            item_name="products",
            relevant_values=[TermTermType.LANDCOVER]
        )
    ]

    products_crop_forage = _get_items_with_relevant_term_type(
        cycles=cycles,
        item_name="products",
        relevant_values=[TermTermType.CROP, TermTermType.FORAGE]
    )
    products_crop_forage = [
        _copy_item_if_exists(
            source=product,
            keys=["startDate", "endDate", "properties"],
            dest={
                "term": linked_node(download_hestia(_get_landCover_term_id(product))),
                "value": 100
            }
        )
        for product in list(filter(_get_landCover_term_id, products_crop_forage))
    ]

    practices = [
        _extract_node_value(
            _include(
                value=practice,
                keys=["term", "value", "startDate", "endDate"]
            )
        ) for practice in _get_items_with_relevant_term_type(
            cycles=cycles,
            item_name="practices",
            relevant_values=[
                TermTermType.WATERREGIME,
                TermTermType.TILLAGE,
                TermTermType.CROPRESIDUEMANAGEMENT,
                TermTermType.LANDUSEMANAGEMENT
            ]
        )
    ]

    relevant_inputs = _get_relevant_inputs(cycles)
    logRequirements(
        site,
        model=MODEL,
        term=None,
        model_key=MODEL_KEY,
        products_crop_forage_ids=log_blank_nodes_id(products_crop_forage),
        products_land_cover_ids=log_blank_nodes_id(products_land_cover),
        practice_ids=log_blank_nodes_id(practices),
        inputs=log_blank_nodes_id(relevant_inputs)
    )
    should_run = any(products_crop_forage + products_land_cover + practices + relevant_inputs)
    logShouldRun(site, MODEL, None, should_run=should_run, model_key=MODEL_KEY)
    return should_run, products_crop_forage + products_land_cover, practices, relevant_inputs


def run(site: dict):
    should_run, products, practices, inputs = _should_run(site)
    return list(map(management, products + practices + inputs)) if should_run else []
