"""Retry logic with exponential backoff."""
import time
import logging
from typing import Callable, TypeVar

logger = logging.getLogger(__name__)

T = TypeVar('T')


def retry_with_backoff(
    func: Callable[..., T],
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 10.0,
    exponential_base: float = 2.0,
) -> T:
    """
    Retry a function with exponential backoff.

    Args:
        func: Function to retry
        max_retries: Maximum number of retries
        base_delay: Initial delay in seconds
        max_delay: Maximum delay in seconds
        exponential_base: Base for exponential backoff

    Returns:
        Result of function call

    Raises:
        Exception: If all retries fail

    Examples:
        >>> def flaky_api_call():
        ...     # Might fail randomly
        ...     return {"status": "success"}
        >>> result = retry_with_backoff(flaky_api_call, max_retries=3)
        >>> result["status"]
        'success'
    """
    last_exception = None
    delay = base_delay

    for attempt in range(max_retries + 1):
        try:
            result = func()
            if attempt > 0:
                logger.info(f"Succeeded after {attempt} retries")
            return result

        except (TimeoutError, ConnectionError) as e:
            # Transient errors - retry
            last_exception = e
            if attempt == max_retries:
                logger.error(f"All {max_retries} retries failed: {type(e).__name__}")
                raise

            logger.warning(
                f"Transient error (attempt {attempt + 1}/{max_retries + 1}): "
                f"{type(e).__name__}. Retrying in {delay:.1f}s..."
            )
            time.sleep(delay)
            delay = min(delay * exponential_base, max_delay)

        except Exception as e:
            # Non-transient errors - don't retry
            logger.error(f"Non-transient error: {type(e).__name__}: {str(e)}")
            raise

    raise last_exception if last_exception else Exception("Unknown error")
