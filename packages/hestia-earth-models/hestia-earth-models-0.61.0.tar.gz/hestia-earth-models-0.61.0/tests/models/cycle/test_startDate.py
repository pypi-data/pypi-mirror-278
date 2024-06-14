from hestia_earth.models.cycle.startDate import _should_run, run


def test_should_run():
    # no endDate => no run
    cycle = {'cycleDuration': 365}
    should_run = _should_run(cycle)
    assert not should_run

    # with startDate missing days => not run
    cycle['endDate'] = '2020-01'
    should_run = _should_run(cycle)
    assert not should_run

    # with endDate full date => run
    cycle['endDate'] = '2020-01-01'
    should_run = _should_run(cycle)
    assert should_run is True


def test_run():
    assert run({'endDate': '2020-01-01', 'cycleDuration': 365}) == '2019-01-01'
