"""
Start Date

This model sets the [Cycle startDate](https://hestia.earth/schema/Cycle#startDate) based on the `endDate` and the
`cycleDuration`. This only works when the `endDate` has been provided to a day precision (`2000-01-01`).
"""
from datetime import timedelta
from hestia_earth.utils.date import is_in_days
from hestia_earth.utils.tools import safe_parse_date

from hestia_earth.models.log import logRequirements, logShouldRun
from . import MODEL

REQUIREMENTS = {
    "Cycle": {
        "endDate": "to day precision",
        "cycleDuration": ""
    }
}
RETURNS = {
    "The startDate as a string": ""
}
MODEL_KEY = 'startDate'


def _run(cycle: dict):
    endDate = safe_parse_date(cycle.get('endDate'))
    cycleDuration = cycle.get('cycleDuration')
    return (endDate - timedelta(days=cycleDuration)).strftime('%Y-%m-%d')


def _should_run(cycle: dict):
    has_endDate = cycle.get('endDate') is not None
    has_day_precision = has_endDate and is_in_days(cycle.get('endDate'))
    has_cycleDuration = cycle.get('cycleDuration') is not None

    logRequirements(cycle, model=MODEL, key=MODEL_KEY,
                    has_endDate=has_endDate,
                    has_day_precision=has_day_precision,
                    has_cycleDuration=has_cycleDuration)

    should_run = all([has_endDate, has_day_precision, has_cycleDuration])
    logShouldRun(cycle, MODEL, None, should_run, key=MODEL_KEY)
    return should_run


def run(cycle: dict): return _run(cycle) if _should_run(cycle) else None
