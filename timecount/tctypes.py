from datetime import timedelta
from dataclasses import dataclass

from typing import Union, List, Tuple


class Entry:
    pass


class EmploymentContract(Entry):
    def __init__(
        self, begin: str, hours_per_week: int, vacation_days_per_year: int,
    ):
        self.begin = begin
        self.vacation_days_per_year = vacation_days_per_year
        self.hours_per_week = timedelta(hours=hours_per_week)
        self.hours_per_workday = timedelta(hours=hours_per_week / 5)


@dataclass
class Balance(Entry):
    reduce_week_target_by_hours: int = 0
    raise_week_target_by_hours: int = 0
    reduce_week_target_by_days: int = 0
    raise_week_target_by_days: int = 0
    add_vacation_days: int = 0
    remove_vacation_days: int = 0
    note: str = ""


DayValues = Union[Tuple[float, float], str]


@dataclass
class Day(Entry):
    def __init__(self, date_str: str, *values):
        self.date_str: str = date_str
        self.values: Tuple[DayValues, ...] = values


@dataclass
class HoliDay(Day):
    def __init__(self, date_str: str, *values: DayValues):
        super().__init__(date_str, *values)


@dataclass
class SickDay(Day):
    def __init__(self, date_str: str, *values: DayValues):
        super().__init__(date_str, *values)


@dataclass
class VacationDay(Day):
    def __init__(self, date_str: str, *values: DayValues):
        super().__init__(date_str, *values)
