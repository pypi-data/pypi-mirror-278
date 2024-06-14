"""
Full Grass Consumption

This model estimates the energetic requirements of ruminants and can be used to estimate the amount of grass they graze.
Source:
[IPCC 2019, Vol.4, Chapter 10](https://www.ipcc-nggip.iges.or.jp/public/2019rf/pdf/4_Volume4/19R_V4_Ch10_Livestock.pdf).
"""
from hestia_earth.schema import TermTermType
from hestia_earth.utils.model import filter_list_term_type
from hestia_earth.utils.tools import list_sum

from hestia_earth.models.log import logRequirements, logShouldRun, debugValues
from hestia_earth.models.utils.input import _new_input
from hestia_earth.models.utils.term import get_wool_terms, get_lookup_value
from hestia_earth.models.utils.completeness import _is_term_type_complete, _is_term_type_incomplete
from hestia_earth.models.utils.property import get_node_property
from .. import MODEL
from ..pastureGrass_utils import (
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
        "completeness.animalPopulation": "True",
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
        "none": {
            "inputs": [{
                "@type": "Input",
                "term.units": "kg",
                "value": "> 0",
                "isAnimalFeed": "True"
            }]
        },
        "optional": {
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
    "animalProduct": ["mjKgEvWoolNetEnergyWoolIpcc2019", "allowedLiveAnimalTermIds"],
    "liveAnimal": [
        "ipcc2019AnimalTypeGrouping",
        "mjDayKgCfiNetEnergyMaintenanceIpcc2019",
        "ratioCPregnancyNetEnergyPregnancyIpcc2019",
        "ratioCNetEnergyGrowthCattleBuffaloIpcc2019",
        "mjKgABNetEnergyGrowthSheepGoatsIpcc2019",
        "isWoolProducingAnimal"
    ],
    "system-liveAnimal-activityCoefficient-ipcc2019": "using animal term @id",
    "crop-property": ["energyDigestibilityRuminants", "energyContentHigherHeatingValue"],
    "crop": "grazedPastureGrassInputId",
    "forage-property": ["energyDigestibilityRuminants", "energyContentHigherHeatingValue"],
    "landCover": "grazedPastureGrassInputId"
}
RETURNS = {
    "Animal": [{
        "Input": [{
            "@type": "Input",
            "term.termType": ["crop", "forage"],
            "value": ""
        }]
    }]
}
MODEL_KEY = 'animal/pastureGrass'


def _input(term_id: str, value: float):
    node = _new_input(term_id, MODEL)
    node['value'] = [value]
    return node


def _sum_liveWeightPerHead(animals: list):
    return list_sum([
        animal.get('value', 0) * get_node_property(animal, 'liveweightPerHead', False).get('value', 0)
        for animal in animals
    ])


def _isNEwool_animal(animal: dict):
    value = get_lookup_value(animal.get('term', {}), 'isWoolProducingAnimal', model=MODEL, model_key=MODEL_KEY)
    return not (not value)


def _is_NEwool_product(product: dict, animal: dict):
    animal_term_ids = get_lookup_value(product, 'allowedLiveAnimalTermIds', model=MODEL, model_key=MODEL_KEY).split(';')
    return animal.get('term', {}).get('@id') in animal_term_ids


def calculate_NEwool(cycle: dict, animal: dict, products: list, total_weight: float) -> float:
    term_id = animal.get('term', {}).get('@id')

    wool_products = [p for p in products if _is_NEwool_product(p.get('term', {}), animal)]
    total_energy = list_sum([
        list_sum(product.get('value', [])) * product_wool_energy(product) for product in wool_products
    ])
    animal_weight = _sum_liveWeightPerHead([animal])

    debugValues(cycle, model=MODEL, term=term_id, model_key=MODEL_KEY,
                total_energy=total_energy,
                animal_liveWeightPerHead=animal_weight,
                total_liveWeightPerHead=total_weight)

    return total_energy * animal_weight/total_weight


def _calculate_GE(
    cycle: dict, animal: dict, REM: float, REG: float, NEwool: float, system: dict
) -> float:
    term_id = animal.get('term', {}).get('@id')

    NEm, NEa, NEl, NEwork, NEp, NEg = get_animal_values(cycle, animal, system)

    NEm_feed, NEg_feed = calculate_NEfeed(animal)
    debugValues(cycle, model=MODEL, term=term_id, model_key=MODEL_KEY,
                NEm_feed=NEm_feed,
                NEg_feed=NEg_feed)

    return (NEm + NEa + NEl + NEwork + NEp - NEm_feed)/REM + (NEg + NEwool - NEg_feed)/REG


def _run_practice(cycle: dict, GE: float, meanECHHV: float):
    def run(practice: dict):
        key = practice.get('key', {})
        key_id = key.get('@id')
        input_term_id = practice_input_id(practice)
        value = (GE / meanECHHV) * (list_sum(practice.get('value', [0])) / 100)

        logRequirements(cycle, model=MODEL, term=input_term_id, model_key=MODEL_KEY,
                        GE=GE,
                        meanECHHV=meanECHHV,
                        key_id=key_id)

        logShouldRun(cycle, MODEL, input_term_id, True, model_key=MODEL_KEY)

        return _input(input_term_id, value)

    return run


def _run_animal(cycle: dict, meanDE: float, meanECHHV: float, system: dict, practices: list):
    REM = calculate_REM(meanDE)
    REG = calculate_REG(meanDE)

    wool_term_ids = get_wool_terms()
    # list of animal product
    wool_products = [p for p in cycle.get('products', []) if p.get('term', {}).get('@id') in wool_term_ids]
    animals = list(filter(_isNEwool_animal, cycle.get('animals', [])))
    total_liveWeightPerHead = _sum_liveWeightPerHead(animals)

    def run(animal: dict):
        term_id = animal.get('term', {}).get('@id')

        NEwool = calculate_NEwool(cycle, animal, wool_products, total_liveWeightPerHead) if (
            total_liveWeightPerHead > 0
        ) else 0
        GE = (_calculate_GE(cycle, animal, REM, REG, NEwool, system) / (meanDE/100)) if all([REM, REG]) else 0

        debugValues(cycle, model=MODEL, term=term_id, model_key=MODEL_KEY,
                    REM=REM,
                    REG=REG,
                    NEwool=NEwool,
                    GE=GE,
                    meanDE=meanDE)

        inputs = list(map(_run_practice(cycle, GE, meanECHHV), practices))
        return animal | {
            'inputs': animal.get('inputs', []) + inputs
        }

    return run


def _run(cycle: dict, meanDE: float, meanECHHV: float, system: dict, practices: list):
    animals = get_animals(cycle)
    return list(map(_run_animal(cycle, meanDE, meanECHHV, system, practices), animals))


def _should_run(cycle: dict, practices: dict):
    systems = filter_list_term_type(cycle.get('practices', []), TermTermType.SYSTEM)
    animalFeed_complete = _is_term_type_complete(cycle, 'animalFeed')
    animalPopulation_complete = _is_term_type_complete(cycle, 'animalPopulation')
    freshForage_incomplete = _is_term_type_incomplete(cycle, 'freshForage')
    all_animals_have_value = all([a.get('value', 0) > 0 for a in cycle.get('animals', [])])

    no_cycle_inputs_feed = all([not input.get('isAnimalFeed', False) for input in cycle.get('inputs', [])])

    meanDE = calculate_meanDE(practices)
    meanECHHV = calculate_meanECHHV(practices)

    should_run = all([
        animalFeed_complete,
        animalPopulation_complete,
        freshForage_incomplete,
        no_cycle_inputs_feed,
        all_animals_have_value,
        len(systems) > 0,
        len(practices) > 0,
        meanDE > 0,
        meanECHHV > 0
    ])

    for term_id in [MODEL_KEY] + [practice_input_id(p) for p in practices]:
        logRequirements(cycle, model=MODEL, term=term_id, model_key=MODEL_KEY,
                        term_type_animalFeed_complete=animalFeed_complete,
                        term_type_animalPopulation_complete=animalPopulation_complete,
                        term_type_freshForage_incomplete=freshForage_incomplete,
                        no_cycle_inputs_feed=no_cycle_inputs_feed,
                        all_animals_have_value=all_animals_have_value,
                        meanDE=meanDE,
                        meanECHHV=meanECHHV)

        logShouldRun(cycle, MODEL, term_id, should_run, model_key=MODEL_KEY)

    return should_run, meanDE, meanECHHV, systems[0] if systems else None


def run(cycle: dict):
    practices = list(filter(should_run_practice(cycle), cycle.get('practices', [])))
    should_run, meanDE, meanECHHV, system = _should_run(cycle, practices)
    return _run(cycle, meanDE, meanECHHV, system, practices) if should_run else []
