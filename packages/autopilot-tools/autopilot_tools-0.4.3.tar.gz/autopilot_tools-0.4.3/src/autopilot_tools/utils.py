from time import sleep
from typing import Callable, TypeVar, Union
from autopilot_tools.logger import logger

T = TypeVar('T')


def retry_command(
        fun: Callable[[], Union[T, None]], times=3,
        test: Callable[[T], bool] = lambda x: x is not None,
        delay: int = 0) -> Union[T, None]:
    exc = None
    for i in range(times):
        res = None
        try:
            res = fun()
            if test(res):
                return res
            # I'm re-raising it later down the line anyways
        except Exception as e:  # pylint: disable=broad-except
            exc = e
        logger.warning(f"Failed command {i+1}/{times} times, "
                    f"result: {res if exc is None else exc}")
        if delay != 0:
            sleep(delay)
    if exc is not None:
        raise exc
    return None
