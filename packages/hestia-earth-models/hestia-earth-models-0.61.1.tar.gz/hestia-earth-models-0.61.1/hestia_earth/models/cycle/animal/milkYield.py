"""
Milk Yield

This model gap-fills the practice "Milk yield per animal X (raw/FPCM)" (e.g. `Milk yield per cow (raw)`) when:
- the practice is added to the Cycle itself, and we can match it with the `term` of an Animal blank node;
- the Animal blank node Term has a lookup value of `kgDayMilkForFeedingOffspring`.
"""
from hestia_earth.schema import TermTermType
from hestia_earth.utils.model import filter_list_term_type
from hestia_earth.utils.tools import non_empty_list, safe_parse_float

from hestia_earth.models.log import logShouldRun, logRequirements, log_blank_nodes_id
from hestia_earth.models.utils.term import get_lookup_value
from hestia_earth.models.utils.practice import _new_practice
from .. import MODEL

REQUIREMENTS = {
    "Cycle": {
        "animals": [{
            "@type": "Animal",
            "term.termType": "liveAnimal"
        }],
        "optional": {
            "practices": [{
                "@type": "Practice",
                "term.termType": "animalManagement"
            }]
        }
    }
}
RETURNS = {
    "Animal": [{
        "practices": [{
            "@type": "Practice",
            "term.termType": "animalManagement"
        }]
    }]
}
LOOKUPS = {
    "liveAnimal": ["milkYieldPracticeTermIds", "kgDayMilkForFeedingOffspring"]
}

MODEL_KEY = 'milkYield'


def _default_practice(animal: dict, practice_term_id: str):
    term = animal.get('term', {})
    value = get_lookup_value(term, LOOKUPS['liveAnimal'][1], model=MODEL, model_key=MODEL_KEY)
    return (_new_practice(practice_term_id) | {'value': [safe_parse_float(value)]}) if value else None


def _run(cycle: dict, animal: dict):
    term = animal.get('term', {})
    term_id = term.get('@id')
    value = get_lookup_value(term, LOOKUPS['liveAnimal'][0], model=MODEL, model_key=MODEL_KEY)
    practice_ids = non_empty_list((value or '').split(';'))
    practices = non_empty_list(
        [p for p in cycle.get('practices', []) if p.get('term', {}).get('@id') in practice_ids] or (
            [_default_practice(animal, practice_ids[0])] if practice_ids else []
        )
    )

    logRequirements(cycle, model=MODEL, term=term_id, model_key=MODEL_KEY,
                    practice_ids=log_blank_nodes_id(practices))

    for practice in practices:
        logShouldRun(cycle, MODEL, practice.get('term', {}).get('@id'), True, model_key=MODEL_KEY)

    return {
        **animal,
        'practices': animal.get('practices', []) + practices
    } if practices else None


def _should_run(cycle: dict):
    animals = filter_list_term_type(cycle.get('animals', []), TermTermType.LIVEANIMAL)
    has_animals = len(animals) > 0

    should_run = all([has_animals])
    logShouldRun(cycle, MODEL, None, should_run, model_key=MODEL_KEY)
    return should_run, animals


def run(cycle: dict):
    should_run, animals = _should_run(cycle)
    return non_empty_list([_run(cycle, a) for a in animals]) if should_run else []
