"""
Functions and routines associated with Enasis Network Common Library.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Any
from typing import Optional

from pydantic import BaseModel

from .common import PARSABLE
from .common import SCHEDULE
from .times import Times



class TimerParams(BaseModel, extra='forbid'):
    """
    Process and validate the core configuration parameters.

    :param timer: Seconds that are used for related timer.
    :param start: Optional time for when the timer started.
    """

    timer: float
    start: Optional[str] = None


    def __init__(
        self,
        timer: int | float,
        start: Optional[PARSABLE] = None,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        if timer is not None:
            timer = float(timer)

        if start is not None:
            start = Times(start)


        data: dict[str, Any] = {
            'timer': timer}

        if start is not None:
            data['start'] = start.subsec


        super().__init__(**data)



class TimersParams(BaseModel, extra='forbid'):
    """
    Process and validate the core configuration parameters.

    :param timers: Seconds that are used for related timer.
    :param data: Keyword arguments passed to Pydantic model.
        Parameter is picked up by autodoc, please ignore.
    """

    timers: dict[str, TimerParams] = {}



class WindowParams(BaseModel, extra='forbid'):
    """
    Process and validate the core configuration parameters.

    :param window: Parameters for defining scheduled time.
    :param start: Determine the start for scheduling window.
    :param stop: Determine the ending for scheduling window.
    :param anchor: Optionally define time anchor for window.
    :param delay: Period of time schedulng will be delayed.
    """

    window: SCHEDULE

    start: Optional[str] = None
    stop: Optional[str] = None
    anchor: Optional[str] = None
    delay: float = 0.0


    def __init__(
        self,
        window: SCHEDULE | int,
        start: Optional[PARSABLE] = None,
        stop: Optional[PARSABLE] = None,
        anchor: Optional[PARSABLE] = None,
        delay: Optional[int | float] = None,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """


        if isinstance(window, int):
            window = {'seconds': window}


        if start is not None:
            start = Times(start)

        if stop is not None:
            stop = Times(stop)

        if anchor is not None:
            anchor = Times(anchor)

        if delay is not None:
            delay = float(delay)


        data: dict[str, Any] = {
            'window': window}

        if start is not None:
            data['start'] = start.subsec

        if stop is not None:
            data['stop'] = stop.subsec

        if anchor is not None:
            data['anchor'] = anchor.subsec

        if delay is not None:
            data['delay'] = delay


        super().__init__(**data)



class WindowsParams(BaseModel, extra='forbid'):
    """
    Process and validate the core configuration parameters.

    :param windows: Parameters for defining scheduled time.
    :param data: Keyword arguments passed to Pydantic model.
        Parameter is picked up by autodoc, please ignore.
    """

    windows: dict[str, WindowParams] = {}
