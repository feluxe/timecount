from datetime import timedelta
from dataclasses import dataclass


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


@dataclass
class Day(Entry):
    def __init__(self, date_str: str, *args):
        self.date_str: str = date_str
        self.args = args


@dataclass
class Holiday(Day):
    def __init__(self, date_str, *args):
        super().__init__(date_str, *args)


@dataclass
class SickDay(Day):
    def __init__(self, date_str, *args):
        super().__init__(date_str, *args)


@dataclass
class VacationDay(Day):
    def __init__(self, date_str, *args):
        super().__init__(date_str, *args)
