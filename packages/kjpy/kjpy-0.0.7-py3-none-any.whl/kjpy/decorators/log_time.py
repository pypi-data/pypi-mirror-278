import time
from functools import wraps
from typing import Any, Callable, Optional

from ..format.format_time import format_time
from ..class_helpers.serializable_csv import SerializableCsv


def _create_function_description(func_name: str, description=""):
    if not description:
        return func_name
    return f"{func_name} - {description}"


class LogTimePassedMemory:
    memory = []

    @classmethod
    def save(cls, filepath: str):
        if not cls.memory:
            with open(filepath, "w") as f:
                f.write("")
                return
        # df = pd.DataFrame(cls.memory)
        cls.memory.sort(key=lambda c: c["elapsed_time"], reverse=True)

        csv_serializer = SerializableCsv(
            all_data=cls.memory,
            column_names=[
                "func_name",
                "description",
                "start_time",
                "elapsed_time",
                "formatted_time",
            ],
        )
        csv_serializer.save("time_passed_unit_tests.csv")


class LogTimePassed(object):
    def __init__(
        self,
        func: Optional[Callable] = None,
        *,
        description: str = "",
        use_only_if_needed: bool = False,
    ) -> None:
        self._func = func
        self._description = description
        self._use_only_if_needed = use_only_if_needed

    def _log_time_passed_decorator(self, func: Callable, description=""):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            response = func(*args, **kwargs)
            elapsed_time = time.time() - start_time
            show_trailing_ms = elapsed_time < 1
            formatted_time = format_time(elapsed_time, show_trailing_ms)
            func_name = func.__name__
            function_description = _create_function_description(func_name, description)
            print(f"Time passed: \t {formatted_time} \t {function_description}")
            stats = {
                "func_name": func_name,
                "description": description,
                "start_time": start_time,
                "elapsed_time": elapsed_time,
                "formatted_time": formatted_time,
            }

            LogTimePassedMemory.memory.append(stats)
            return response

        return wrapper

    def __call__(self, func: Optional[Callable] = None, *args) -> Any:
        func = func or self._func
        if self._use_only_if_needed:
            return func
        return self._log_time_passed_decorator(func=func, description=self._description)


def _decorator_with_any_args(*args, wrapper: Optional[Callable]):
    assert len(args) == 1
    if wrapper is not None and len(args) == 1 and callable(args[0]):
        func = args[0]
        return wrapper(func)()

    def inner(func: Callable):
        if wrapper is None:
            return func
        return wrapper(func, *args)

    return inner


def log_time_passed(*args):
    return _decorator_with_any_args(*args, wrapper=LogTimePassed)


# def log_time_passed(*args, **kwargs):
#     return LogTimePassed(*args, **kwargs)


# def log_time_passed_if_required(*args, **kwargs):
#     return LogTimePassed(*args, **kwargs, use_only_if_needed=True)
