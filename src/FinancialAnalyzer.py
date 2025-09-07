
import time
import functools
from typing import Any, Callable, List, Union, Dict

# --- Decorators ---
def timer_decorator(func: Callable) -> Callable:
    """
    A decorator that measures the execution time of a function.

    Args:
        func (Callable): The function to be timed.

    Returns:
        Callable: The decorated function.
    """
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        print(f"Function {func.__name__!r} finished in {run_time:.4f} seconds")
        return result
    return wrapper

