"""
Start Date

This model updates the [Cycle startDate](https://hestia.earth/schema/Cycle#startDate) to be in the following format:
`YYYY-MM-DD`.
"""
from hestia_earth.utils.date import is_in_days
from hestia_earth.utils.tools import non_empty_list

from hestia_earth.models.log import logRequirements, logShouldRun
from . import MODEL

REQUIREMENTS = {
    "Cycle": {
        "startDate": ""
    }
}
RETURNS = {
    "The startDate as a string": ""
}
MODEL_KEY = 'startDate'


def _run(cycle: dict):
    value = cycle.get('startDate')
    return '-'.join(non_empty_list([value, '01' if len(value) == 4 else '', '01']))


def _should_run(cycle: dict):
    has_startDate = cycle.get('startDate') is not None
    has_incorrect_format = has_startDate and not is_in_days(cycle.get('startDate'))

    logRequirements(cycle, model=MODEL, key=MODEL_KEY,
                    has_startDate=has_startDate,
                    has_incorrect_format=has_incorrect_format)

    should_run = all([has_startDate, has_incorrect_format])
    logShouldRun(cycle, MODEL, None, should_run, key=MODEL_KEY)
    return should_run


def run(cycle: dict): return _run(cycle) if _should_run(cycle) else None
