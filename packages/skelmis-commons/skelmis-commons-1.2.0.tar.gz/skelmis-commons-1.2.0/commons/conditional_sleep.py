import asyncio
import functools
from typing import Union, Callable, Any, Coroutine


async def sleep_with_condition(
    seconds: float,
    condition: Union[
        functools.partial,
        Callable[[Any], bool],
        Callable[[Any], Coroutine[Any, Any, bool]],
    ],
    *,
    interval: float = 5,
) -> None:
    """Sleep until either condition is True or we run out of seconds

    Parameters
    ----------
    seconds: float
        How long to sleep for up to
    condition
        Pass either:
        - A sync function to call which returns a bool
        - An async function to call which returns a bool

        .. note::

            If you wish to use arguments in you functions,
            pass an instance of :class:`functools.partial`
    interval: float
        How long to sleep in-between each condition check.

        Defaults to 5 seconds.
    """
    if asyncio.iscoroutinefunction(condition):
        wrapped_condition = condition
    elif callable(condition) or isinstance(condition, functools.partial):

        async def wrapped_condition():
            return condition()

    else:
        raise TypeError("Unknown input argument")

    remaining_seconds = seconds
    while remaining_seconds > 0:
        remaining_seconds -= interval
        await asyncio.sleep(interval)

        if await wrapped_condition():
            return
