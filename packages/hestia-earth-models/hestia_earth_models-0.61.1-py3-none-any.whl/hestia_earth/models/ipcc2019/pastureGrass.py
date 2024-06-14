"""
Full Grass Consumption

This model estimates the energetic requirements of ruminants and can be used to estimate the amount of grass they graze.
Source:
[IPCC 2019, Vol.4, Chapter 10](https://www.ipcc-nggip.iges.or.jp/public/2019rf/pdf/4_Volume4/19R_V4_Ch10_Livestock.pdf).
"""
from hestia_earth.schema import TermTermType
from hestia_earth.utils.model import filter_list_term_type
from hestia_earth.utils.tools import list_sum

from hestia_earth.models.log import logRequirements, logShouldRun
from hestia_earth.models.utils.input import _new_input
from hestia_earth.models.utils.term import get_wool_terms
from hestia_earth.models.utils.completeness import _is_term_type_complete, _is_term_type_incomplete
from . import MODEL
from .pastureGrass_utils import (
    practice_input_id,
    should_run_practice,
    calculate_meanDE,
    calculate_meanECHHV,
    calculate_REM,
    calculate_REG,
    calculate_NEfeed,
    product_wool_energy,
    get_animals,
    get_animal_values
)

REQUIREMENTS = {
    "Cycle": {
        "completeness.animalFeed": "True",
        "completeness.animalPopulation": "False",
        "completeness.freshForage": "False",
        "site": {
            "@type": "Site",
            "siteType": "permanent pasture"
        },
        "practices": [{
            "@type": "Practice",
            "value": "",
            "term.@id": "pastureGrass",
            "key": {
                "@type": "Term",
                "term.termType": "landCover"
            }
        }],
        "animals": [{
            "@type": "Animal",
            "value": "> 0",
            "term.termType": "liveAnimal",
            "referencePeriod": "average",
            "properties": [{
                "@type": "Property",
                "value": "",
                "term.@id": [
                    "liveweightPerHead",
                    "weightAtMaturity"
                ]
            }],
            "optional": {
                "properties": [{
                    "@type": "Property",
                    "value": "",
                    "term.@id": [
                        "hoursWorkedPerDay",
                        "pregnancyRateTotal",
                        "animalsPerBirth"
                    ]
                }],
                "inputs": [{
                    "@type": "Input",
                    "term.units": "kg",
                    "value": "> 0",
                    "optional": {
                        "properties": [{
                            "@type": "Property",
                            "value": "",
                            "term.@id": ["neutralDetergentFibreContent", "energyContentHigherHeatingValue"]
                        }]
                    }
                }],
                "practices": [{
                    "@type": "Practice",
                    "value": "",
                    "term.termType": "animalManagement",
                    "properties": [{
                        "@type": "Property",
                        "value": "",
                        "term.@id": "fatContent"
                    }]
                }]
            }
        }],
        "optional": {
            "inputs": [{
                "@type": "Input",
                "term.units": "kg",
                "value": "> 0",
                "isAnimalFeed": "True",
                "optional": {
                    "properties": [{
                        "@type": "Property",
                        "value": "",
                        "term.@id": ["neutralDetergentFibreContent", "energyContentHigherHeatingValue"]
                    }]
                }
            }],
            "products": [{
                "@type": "Product",
                "value": "",
                "term.@id": "animalProduct"
            }]
        }
    }
}
LOOKUPS = {
    "animalManagement": [
        "mjKgEvMilkIpcc2019"
    ],
    "animalProduct": ["mjKgEvWoolNetEnergyWoolIpcc2019"],
    "liveAnimal": [
        "ipcc2019AnimalTypeGrouping",
        "mjDayKgCfiNetEnergyMaintenanceIpcc2019",
        "ratioCPregnancyNetEnergyPregnancyIpcc2019",
        "ratioCNetEnergyGrowthCattleBuffaloIpcc2019",
        "mjKgABNetEnergyGrowthSheepGoatsIpcc2019"
    ],
    "system-liveAnimal-activityCoefficient-ipcc2019": "using animal term @id",
    "crop-property": ["energyDigestibilityRuminants", "energyContentHigherHeatingValue"],
    "crop": "grazedPastureGrassInputId",
    "forage-property": ["energyDigestibilityRuminants", "energyContentHigherHeatingValue"],
    "landCover": "grazedPastureGrassInputId"
}
RETURNS = {
    "Input": [{
        "term.termType": ["crop", "forage"],
        "value": ""
    }]
}
MODEL_KEY = 'pastureGrass'


def _input(term_id: str, value: float):
    node = _new_input(term_id, MODEL)
    node['value'] = [value]
    return node


def _sum_values(values: list, index=0): return list_sum([v[index] for v in values])


def calculate_NEwool(cycle: dict) -> float:
    term_ids = get_wool_terms()
    products = [p for p in cycle.get('products', []) if p.get('term', {}).get('@id') in term_ids]
    product_values = [
        (list_sum(p.get('value', [])), product_wool_energy(p)) for p in products
    ]
    return sum([value * lookup_value for (value, lookup_value) in product_values])


def _calculate_GE(
    cycle: dict, animals: list, REM: float, REG: float, NEwool: float, NEm_feed: float, NEg_feed: float, system: dict
) -> float:
    values = [get_animal_values(cycle, animal, system) for animal in animals]
    NEm = _sum_values(values, 0)
    NEa = _sum_values(values, 1)
    NEl = _sum_values(values, 2)
    NEwork = _sum_values(values, 3)
    NEp = _sum_values(values, 4)
    NEg = _sum_values(values, 5)
    return (NEm + NEa + NEl + NEwork + NEp - NEm_feed)/REM + (NEg + NEwool - NEg_feed)/REG


def _run_practice(cycle: dict, meanDE: float, meanECHHV: float, system: dict):
    animals = get_animals(cycle)
    REM = calculate_REM(meanDE)
    REG = calculate_REG(meanDE)
    NEwool = calculate_NEwool(cycle)
    NEm_feed, NEg_feed = calculate_NEfeed(cycle)
    GE = (
        _calculate_GE(cycle, animals, REM, REG, NEwool, NEm_feed, NEg_feed, system) / (meanDE/100)
    ) if all([REM, REG]) else 0

    def run(practice: dict):
        key = practice.get('key', {})
        key_id = key.get('@id')
        input_term_id = practice_input_id(practice)
        value = (GE / meanECHHV) * (list_sum(practice.get('value', [0])) / 100)

        logRequirements(cycle, model=MODEL, term=input_term_id, model_key=MODEL_KEY,
                        REM=REM,
                        REG=REG,
                        NEwool=NEwool,
                        NEm_feed=NEm_feed,
                        NEg_feed=NEg_feed,
                        GE=GE,
                        key_id=key_id)

        logShouldRun(cycle, MODEL, input_term_id, True, model_key=MODEL_KEY)

        return _input(input_term_id, value)

    return run


def _should_run(cycle: dict, practices: dict):
    systems = filter_list_term_type(cycle.get('practices', []), TermTermType.SYSTEM)
    animalFeed_complete = _is_term_type_complete(cycle, 'animalFeed')
    animalPopulation_incomplete = _is_term_type_incomplete(cycle, 'animalPopulation')
    freshForage_incomplete = _is_term_type_incomplete(cycle, 'freshForage')
    all_animals_have_value = all([a.get('value', 0) > 0 for a in cycle.get('animals', [])])

    meanDE = calculate_meanDE(practices)
    meanECHHV = calculate_meanECHHV(practices)

    should_run = all([
        animalFeed_complete,
        animalPopulation_incomplete,
        freshForage_incomplete,
        all_animals_have_value,
        len(systems) > 0,
        len(practices) > 0,
        meanDE > 0,
        meanECHHV > 0
    ])

    for term_id in [MODEL_KEY] + [practice_input_id(p) for p in practices]:
        logRequirements(cycle, model=MODEL, term=term_id, model_key=MODEL_KEY,
                        term_type_animalFeed_complete=animalFeed_complete,
                        term_type_animalPopulation_incomplete=animalPopulation_incomplete,
                        term_type_freshForage_incomplete=freshForage_incomplete,
                        all_animals_have_value=all_animals_have_value,
                        meanDE=meanDE,
                        meanECHHV=meanECHHV)

        logShouldRun(cycle, MODEL, term_id, should_run, model_key=MODEL_KEY)

    return should_run, meanDE, meanECHHV, systems[0] if systems else None


def run(cycle: dict):
    practices = list(filter(should_run_practice(cycle), cycle.get('practices', [])))
    should_run, meanDE, meanECHHV, system = _should_run(cycle, practices)
    return list(map(_run_practice(cycle, meanDE, meanECHHV, system), practices)) if should_run else []
