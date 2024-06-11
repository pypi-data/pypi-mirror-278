import inspect
import time
import warnings

from typing import Type, Union, Callable, Tuple


class NotImplementedMethodError(Exception):
    def __init__(self, function_name: str = 'function'):
        message = f"Method {function_name} is not implemented."
        super().__init__(message)


def todo(alert: Union[Callable[[str], None], Type[Exception]] = None) -> None:
    """
   A function to replace the 'pass' keyword, ensuring that developers do not forget to handle code blocks.

   :param alert: A callable that takes a string as an argument and performs an action (e.g., logging or raising an exception),
                 or a type of exception to raise. If not provided, a default exception is raised.
   :type alert: Callable[[str], None] or Type[Exception], optional

   :return: None
   :rtype: None

   This function captures the name of the parent function where it is called and either raises an exception
   or triggers the provided alert with a message indicating that the method is not implemented.
   It is intended to be used as a placeholder for future code implementation, ensuring that no code block is left empty.
   """
    current_frame = inspect.currentframe()
    parent_frame = current_frame.f_back
    parent_function_name: str = parent_frame.f_code.co_name
    if not alert:
        raise NotImplementedMethodError(parent_function_name)
    else:
        alert(f"Method {parent_function_name} is not implemented.")


def no_error(throw: Callable[[str], None] = print,
             format: str = "Error: {}",
             exceptions: Union[Tuple[Type[Exception], ...], Type[Exception]] = Exception):
    """
    A decorator that allows functions to ignore certain exceptions.

    :param throw: A callable that takes a string input. This is used to handle the error message, e.g., print it or log it.
    :param format: A string that defines the format of the error message. The error message will be inserted at the '{}' placeholder.
    :param exceptions: The type(s) of exceptions to catch. Can be a single exception type or a tuple of exception types.
    """
    def wrapper(func):
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except exceptions as e:
                throw(format.format(e))
        return inner
    return wrapper


def retry(times: int,
          delay: float = 0,
          exceptions: Union[Tuple[Type[Exception], ...], Type[Exception]] = Exception,
          final: Callable[[], None] = None):
    """
    Retry calling the decorated function using an exponential backoff.

    :param times: The number of times to retry the function call. If times is greater than or equal to 0, it means the function will be retried times+1 times. If times is less than 0, it means the function will be retried indefinitely.
    :param delay: The initial delay between retries in seconds. The delay will be doubled after each retry.
    :param exceptions: The exception or tuple of exceptions to catch. If Exception is used, it should be avoided with negative times to prevent an infinite loop.
    :param final: A function to call after all retries have been exhausted.
    """
    if times < 0:
        if (exceptions is Exception) or (isinstance(exceptions, tuple) and Exception in exceptions):
            warnings.warn("Using Exception with negative times can lead to an infinite loop.", RuntimeWarning)

    def wrapper(func):
        def inner(*args, **kwargs):
            t = times
            while True:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if t == 0:
                        if final:
                            final()
                        raise e
                    if t > 0:
                        t -= 1
                    time.sleep(delay)
        return inner
    return wrapper


def timer():
    """
    A decorator that measures the execution time of a function.
    :return: The execution time of the function + the result of the function.
    """
    def wrapper(func):
        def inner(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            end = time.perf_counter()
            return end-start, result
        return inner
    return wrapper
