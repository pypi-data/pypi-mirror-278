from hestia_earth.models.cycle.startDate import _should_run, run


def test_should_run():
    # no startDate => no run
    cycle = {}
    should_run = _should_run(cycle)
    assert not should_run

    # with startDate full date => no run
    cycle['startDate'] = '2020-01-01'
    should_run = _should_run(cycle)
    assert not should_run

    # with startDate missing days => run
    cycle['startDate'] = '2020-01'
    should_run = _should_run(cycle)
    assert should_run is True


def test_run():
    assert run({'startDate': '2020-01'}) == '2020-01-01'
