import asyncio
import time
from typing import Any, Callable, Coroutine

from observe.logger import get_logger

logger = get_logger()


class InternalPredictionError(Exception):
    pass


class PredictionError(Exception):
    pass


def exponential_backoff(func, max_retries=2):
    delay = 2  # Initial delay is seconds
    for i in range(max_retries):
        try:
            return func()
        except PredictionError as e:
            raise e
        except Exception as e:
            logger.error(
                f"Attempt failed. Retrying in {delay} seconds...",
                error=str(e),
                i=i + 1,
                delay=delay,
            )
            time.sleep(delay)
            delay *= 2  # Double the delay each time we retry

    logger.error("All attempts failed")
    raise PredictionError("All attempts failed")


AsyncCallback = Callable[[], Coroutine[Any, Any, Any]]


async def async_exponential_backoff(
    func: AsyncCallback, max_retries=2, initial_delay=2
):
    delay = initial_delay  # Initial delay in seconds
    for i in range(max_retries):
        try:
            return await func()
        except PredictionError as e:
            raise e
        except Exception as e:
            logger.error(
                f"Attempt failed. Retrying in {delay} seconds...",
                error=str(e),
                i=i + 1,
                delay=delay,
            )
            await asyncio.sleep(delay)
            delay *= 2  # Double the delay each time we retry

    logger.error("All attempts failed")
    raise PredictionError("All attempts failed")
