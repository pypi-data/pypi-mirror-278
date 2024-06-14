from datetime import datetime, timedelta
from typing import Callable, TypeAlias

Buffer: TypeAlias = bytes

ConditionType: TypeAlias = Callable[[list[Buffer]], bool]

_DateTimeFuncType: TypeAlias = Callable[[Buffer], datetime]


def get_size_condition(size: int) -> ConditionType:
    return lambda data: len(data) <= size


def get_time_delta_condition(
    datetime_func: _DateTimeFuncType,
    delta: timedelta,
) -> ConditionType:
    return lambda data: datetime_func(data[-1]) - datetime_func(data[0]) < delta


def get_per_second_condition(
    datetime_func: _DateTimeFuncType,
) -> ConditionType:
    return lambda data: (
        datetime_func(data[-1]) - datetime_func(data[0]) < timedelta(seconds=1)
        and datetime_func(data[-1]).second == datetime_func(data[0]).second
    )


def get_per_minute_condition(
    datetime_func: _DateTimeFuncType,
) -> ConditionType:
    return lambda data: (
        datetime_func(data[-1]) - datetime_func(data[0]) < timedelta(minutes=1)
        and datetime_func(data[-1]).minute == datetime_func(data[0]).minute
    )


def get_per_hour_condition(
    datetime_func: _DateTimeFuncType,
) -> ConditionType:
    return lambda data: (
        datetime_func(data[-1]) - datetime_func(data[0]) < timedelta(hours=1)
        and datetime_func(data[-1]).hour == datetime_func(data[0]).hour
    )


def get_per_day_condition(
    datetime_func: _DateTimeFuncType,
) -> ConditionType:
    return lambda data: (
        datetime_func(data[-1]) - datetime_func(data[0]) < timedelta(days=1)
        and datetime_func(data[-1]).day == datetime_func(data[0]).day
    )
