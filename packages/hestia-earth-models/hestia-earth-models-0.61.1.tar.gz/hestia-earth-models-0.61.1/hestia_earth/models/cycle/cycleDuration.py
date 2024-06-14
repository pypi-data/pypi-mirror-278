"""
Cycle duration

This model calculates the cycle duration using:
* the `endDate` and the `startDate` if both are provided with a day precision;
* for temporary crops, using the `croppingIntensity` if provided;
* for permanent crops, the duration is set to `365`.
"""
from hestia_earth.schema import TermTermType
from hestia_earth.utils.model import find_term_match, find_primary_product
from hestia_earth.utils.date import diff_in_days

from hestia_earth.models.log import logRequirements, logShouldRun
from hestia_earth.models.utils.crop import get_crop_grouping_fao
from . import MODEL

REQUIREMENTS = {
    "Cycle": {
        "endDate": "",
        "optional": {
            "startDate": "",
            "products": {
                "@type": "Product",
                "primary": "True",
                "term.termType": "crop"
            },
            "practices": [{"@type": "Practice", "value": "", "term.@id": "croppingIntensity"}]
        }
    }
}
RETURNS = {
    "a `number` or `None` if requirements are not met": ""
}
LOOKUPS = {
    "crop": "cropGroupingFAO"
}
MODEL_KEY = 'cycleDuration'
DEFAULT_DURATION = 365


def _run_by_dates(cycle: dict):
    start_date = cycle.get('startDate')
    end_date = cycle.get('endDate')
    return diff_in_days(start_date, end_date)


def _should_run_by_dates(cycle: dict):
    start_date = cycle.get('startDate', '')
    start_date_has_day = len(start_date) == 10
    end_date = cycle.get('endDate', '')
    end_date_has_day = len(start_date) == 10

    logRequirements(cycle, model=MODEL, key=MODEL_KEY, by='dates',
                    start_date_has_day=start_date_has_day,
                    start_date=start_date,
                    end_date_has_day=end_date_has_day,
                    end_date=end_date)

    should_run = all([start_date_has_day, end_date_has_day])
    logShouldRun(cycle, MODEL, None, should_run, key=MODEL_KEY, by='dates')
    return should_run


def _run_by_crop(cycle: dict):
    product = find_primary_product(cycle)
    grouping = get_crop_grouping_fao(MODEL, MODEL_KEY, product.get('term', {}))
    is_permanent_crop = grouping == 'Permanent crops'
    croppingIntensity = find_term_match(cycle.get('practices', []), 'croppingIntensity').get('value', [1])[0]
    return DEFAULT_DURATION * (1 if is_permanent_crop else croppingIntensity)


def _should_run_by_crop(cycle: dict):
    product = find_primary_product(cycle) or {}
    product_term_type = product.get('term', {}).get('termType')
    primary_product_is_crop = product_term_type == TermTermType.CROP.value

    logRequirements(cycle, model=MODEL, key=MODEL_KEY, by='product',
                    primary_product_is_crop=primary_product_is_crop)

    should_run = all([primary_product_is_crop])
    logShouldRun(cycle, MODEL, None, should_run, key=MODEL_KEY, by='product')
    return should_run


def run(cycle: dict):
    return _run_by_dates(cycle) if _should_run_by_dates(cycle) else (
        _run_by_crop(cycle) if _should_run_by_crop(cycle)
        else None
    )
