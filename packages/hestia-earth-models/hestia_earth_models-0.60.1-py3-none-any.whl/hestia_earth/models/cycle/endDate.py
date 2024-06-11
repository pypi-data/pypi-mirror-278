"""
Start Date

This model updates the [Cycle endDate](https://hestia.earth/schema/Cycle#endDate) to be in the following format:
`YYYY-MM-DD`.
"""
from hestia_earth.utils.date import is_in_days
from hestia_earth.utils.tools import non_empty_list

from hestia_earth.models.log import logRequirements, logShouldRun
from hestia_earth.models.utils import last_day_of_month
from . import MODEL

REQUIREMENTS = {
    "Cycle": {
        "endDate": ""
    }
}
RETURNS = {
    "The endDate as a string": ""
}
MODEL_KEY = 'endDate'


def _last_day(date: str):
    last_day = last_day_of_month(date[0:4], date[5:7])
    return str(last_day.day)


def _run(cycle: dict):
    value = cycle.get('endDate')
    month = '12' if len(value) == 4 else ''
    day = '31' if len(value) == 4 else _last_day(value)
    return '-'.join(non_empty_list([value, month, day]))


def _should_run(cycle: dict):
    has_endDate = cycle.get('endDate') is not None
    has_incorrect_format = has_endDate and not is_in_days(cycle.get('endDate'))

    logRequirements(cycle, model=MODEL, key=MODEL_KEY,
                    has_endDate=has_endDate,
                    has_incorrect_format=has_incorrect_format)

    should_run = all([has_endDate, has_incorrect_format])
    logShouldRun(cycle, MODEL, None, should_run, key=MODEL_KEY)
    return should_run


def run(cycle: dict): return _run(cycle) if _should_run(cycle) else None
