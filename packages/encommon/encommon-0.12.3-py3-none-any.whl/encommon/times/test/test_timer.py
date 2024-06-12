"""
Functions and routines associated with Enasis Network Common Library.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from time import sleep

from pytest import fixture

from ..timer import Timer
from ..times import Times
from ...types import inrepr
from ...types import instr



@fixture
def timer() -> Timer:
    """
    Construct the instance for use in the downstream tests.

    :returns: Newly constructed instance of related class.
    """

    return Timer(1)



def test_Timer(
    timer: Timer,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param timer: Primary class instance for timer object.
    """


    attrs = list(timer.__dict__)

    assert attrs == [
        '_Timer__timer',
        '_Timer__times']


    assert inrepr(
        'timer.Timer object',
        timer)

    assert hash(timer) > 0

    assert instr(
        'timer.Timer object',
        timer)


    assert timer.timer == 1

    assert timer.times >= Times('-1s')

    assert timer.since <= 1

    assert timer.remains <= 1

    assert not timer.ready()


    sleep(1)

    assert timer.since > 1

    assert timer.remains == 0

    assert timer.ready()

    assert not timer.ready()

    timer.update('1980-01-01')

    assert timer.ready()

    assert not timer.ready()
