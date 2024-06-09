"""
vulcan_utils/decorator.py

This module provides decorators for logging, retrying, JSON serialization, rate limiting, 
and environment variable restriction for function execution.
"""


import json
import os
import time
from functools import wraps
from typing import Any, Callable, Optional, TypeVar, Union

from .encoder import Encoder
from .logger import Logger

# TypeVar for decorator type preservation
F = TypeVar('F', bound=Callable[..., Any])


def _call_message(func: Callable[..., Any], *args: Any, **kwargs: Any) -> str:
    """
    Constructs a log message string for function calls, including function name,
    positional arguments, and keyword arguments.

    Args:
        func (Callable[..., Any]): The function being called.
        *args (Any): Positional arguments passed to the function.
        **kwargs (Any): Keyword arguments passed to the function.

    Returns:
        A formatted log message string.
    """

    log_message_parts = [f"{func.__name__} call:"]
    if args:
        log_message_parts.append(f"args:{args}")
    if kwargs:
        log_message_parts.append(f"kwargs:{kwargs}")
    return ' '.join(log_message_parts)


def _return_message(func: Callable[..., Any], result: Any) -> str:
    """
    Constructs a log message string for function returns, including function name and the 
    serialized return value.

    Args:
        func (Callable[..., Any]): The function that returned a value.
        result (Any): The return value of the function.

    Returns:
        A formatted log message string with the serialized return value.
    """

    json_result = json.dumps(result, cls=Encoder, ensure_ascii=False)
    return f"{func.__name__} return: {json_result} {type(result)}"


def _log_func(logger: Logger, level: str) -> Callable[[str], None]:
    """
    Retrieves the appropriate logging function based on the specified log level.

    Args:
        logger (logger.Logger): An instance of Logger configured for logging messages.
        level (str): A string representing the logging level.

    Returns:
        A logging function from the Logger instance corresponding to the specified level.
    """

    levels = {
        "DEBUG": logger.debug,
        "INFO": logger.info,
        "WARNING": logger.warning,
        "CRITICAL": logger.critical,
        "ERROR": logger.error,
    }
    return levels.get(level.upper(), logger.debug)


def log(
    _func: Optional[F] = None,
        *,
        condition: bool = True,
        level: str = "DEBUG"
) -> Union[Callable[[F], F], F]:
    """
    A decorator that logs the call and return of functions, including execution time.
    Logging can be conditioned on a boolean expression.

    Args:
        _func (Callable[..., Any]): The function to be decorated. If None, other parameters are 
            allowed to be specified first.
        condition (bool): A boolean flag to determine if logging should occur, defaults to True.
        level (str): A string indicating the logging level, defaults to "DEBUG".

    Returns:
        The decorated function with logging capabilities added.
    """

    def decorator_log(func: F):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = None
            if condition:
                start_time = time.time()
                logger = Logger(func.__module__)
                log_func = _log_func(logger, level)
                log_func(_call_message(func, *args, **kwargs))
                result = func(*args, **kwargs)
                log_func(_return_message(func, result))
                end_time = time.time()
                execution_time_ms = round(
                    (end_time - start_time) * 1000,
                    ndigits=4
                )
                log_func(
                    f"{func.__name__} executed: {execution_time_ms} milliseconds")
            else:
                result = func(*args, **kwargs)
            return result
        return wrapper
    if _func is None:
        return decorator_log
    else:
        return decorator_log(_func)


def retry(
        _func: Optional[F] = None,
        *,
        retries: int = 3,
        delay: Union[int, float] = 1,
        infinite: bool = False
) -> Union[Callable[[F], F], F]:
    """
    Decorator to retry a function if it raises an exception. Optionally retries the function 
        indefinitely if `infinite` is True. If not, it retries a specified number of times with a 
        given delay between each attempt.

    Args:
        _func (Callable[..., Any]): The function to be decorated. If None, other parameters can be 
            specified first.
        retries (int): The maximum number of retries before giving up and raising the exception if 
            not infinite.
        delay (Union[int, float]): The delay between retries in seconds, can be an integer or a 
            float for partial seconds.
        infinite (bool): If True, the function will retry indefinitely, defaults to False.

    Returns:
        The decorated function that will retry on exceptions, or raises the last encountered 
            exception if all retries fail and not infinite.

    Raises:
        Exception: The last exception encountered if the retry attempts exceed the specified limit 
            and not infinite.
    """

    def decorator_retry(func: F):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except Exception as e:  # pylint: disable=broad-except
                    logger = Logger(__name__)
                    if infinite:
                        logger.warning(
                            f"{func.__name__} failed, retrying indefinitely: {e}"
                        )
                        time.sleep(delay)
                    else:
                        if attempt < retries:
                            logger.warning(
                                f"{func.__name__} failed, retrying: {e}, " +
                                f"attempts left: {retries - attempt - 1}"
                            )
                            time.sleep(delay)
                            attempt += 1
                        else:
                            logger.error(
                                f"{func.__name__} retry attempts failed: {e}")
                            raise e
        return wrapper
    if _func is not None:
        return decorator_retry(_func)
    return decorator_retry


def to_json(_func: Union[Callable[[F], F], F] = None) -> Union[Callable[[F], F], F]:
    """
    A decorator that serializes the return value of the decorated function to JSON using a custom 
        encoder.

    Args:
        _func (Optional[Callable[[F], F]]): The function to decorate. If None, allows other 
            parameters to be specified first as keyword arguments.

    Returns:
        Callable[[F], F]: The decorated function with its return value serialized as a JSON string.
    """

    def decorator_to_json(func: F) -> F:
        @wraps(func)
        def wrapper(*args, **kwargs) -> str:
            logger = Logger(func.__module__)
            result = func(*args, **kwargs)
            json_result = json.dumps(result, cls=Encoder, ensure_ascii=False)
            logger.debug(f"{func.__name__} JSON return: {json_result}")
            return json_result
        return wrapper
    if _func is not None:
        return decorator_to_json(_func)
    return decorator_to_json


def rate_limit(limit: int, interval: float):
    """
    Decorator to rate limit the execution of a function. Allows a burst of 'limit' calls,
    and then enforces a cooldown period of 'interval' seconds before allowing another burst.

    Args:
        limit (int): Maximum number of calls allowed within the burst.
        interval (float): Cooldown interval (in seconds) after a burst before resetting the limit.
    """

    def decorator(func):
        call_times = []
        first_call_time = None

        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal first_call_time
            now = time.time()
            if first_call_time and now - first_call_time > interval:
                call_times.clear()
                first_call_time = None
            if not first_call_time:
                first_call_time = now
            if len(call_times) < limit:
                call_times.append(now)
                return func(*args, **kwargs)
            else:
                logger = Logger(func.__module__)
                logger.error(f"Rate limit exceeded for {func.__name__}")
                return
        return wrapper
    return decorator


def env(
        _func: Optional[F] = None,
        *,
        variable: str,
        value: Optional[str] = None
) -> Union[Callable[[F], F], F]:
    """
    A decorator that restricts function execution based on the presence or value of an environment 
        variable.

    Args:
        _func (Callable[..., Any], optional): The function to be decorated. If None, allows 
            decorator to be used with arguments.
        variable (str): The environment variable name to check.
        value (str, optional): The specific value the environment variable must have for the 
            function to execute. If not specified, the existence of the variable is enough to 
            allow execution.

    Returns:
        Callable[[F], F]: The decorated function, which will only execute if the conditions are 
            met. Returns None if conditions are not met.
    """

    def decorator_env(func: F) -> F:
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger = Logger(func.__module__)
            env_value = os.getenv(variable)
            if env_value is not None:
                if value is None or env_value == value:
                    logger.debug(
                        f"{func.__name__} execution allowed: '{variable}' set to '{env_value}'.")
                    return func(*args, **kwargs)
                else:
                    logger.warning(
                        f"{func.__name__} blocked: '{variable}' value '{env_value}' " +
                        f"does not match required '{value}'."
                    )
            else:
                logger.warning(
                    f"{func.__name__} blocked: Environment variable '{variable}' not set.")
            return None
        return wrapper
    if _func is None:
        return decorator_env
    return decorator_env(_func)
