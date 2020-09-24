from dataclasses import dataclass, field as dc_field
import sys
import datetime
from datetime import timedelta
from typing import List, Optional, Tuple
from .tctypes import *

WEEKS_PER_YEAR = 52.1429


class C:
    GREY = "\033[37m"
    GREY_DA = f"\x1b[38;2;{120};{120};{120}m"
    BLOCK = f"\x1b[38;2;{150};{130};{150}m"
    TIME = f"\x1b[38;2;{190};{140};{4}m"
    OVER = f"\x1b[38;2;{252};{147};{4}m"
    DATE = f"\x1b[38;2;{150};{150};{150}m"
    MONTH_NUM = "\033[96m"
    WEEKNUM_DA = "\33[34m"
    WEEKNUM_LI = "\33[94m"

    RED_TYPE = f"\x1b[38;2;{200};{50};{4}m"
    HOLIDAY = f"\x1b[38;2;{70};{160};{70}m"
    VACADAY = f"\x1b[38;2;{30};{160};{160}m"
    SICKDAY = f"\x1b[38;2;{230};{120};{50}m"

    ERROR = f"\x1b[38;2;{250};{100};{4}m"
    ITALIC = "\33[3m"

    RS = "\033[0m"


def get_date_from_str(day_month_year: str) -> datetime.date:
    """
    Turn this "01-04-2020" into a datetime.date().
    """
    return datetime.date(*reversed([int(x) for x in day_month_year.split("-")]))


def get_day_data(values: Tuple[DayValues, ...]) -> Tuple[timedelta, str, str]:
    day_total_hours = timedelta(hours=0, minutes=0)
    blocks_str = ""
    msg = ""

    for block in values:

        if isinstance(block, str):
            msg += block
            continue

        if not isinstance(block, tuple) or len(block) != 2:
            print(f"{C.RED_TYPE}WARNING: Incomplete Time Block.{C.RS}")
            continue

        start_raw = str(f"{block[0]:.2f}").split(".")  # -> [10, 30]
        end_raw = str(f"{block[1]:.2f}").split(".")  # -> [10, 30]

        start_h, start_m = int(start_raw[0]), int(start_raw[1])
        end_h, end_m = int(end_raw[0]), int(end_raw[1])

        blocks_str += f"[{start_h:02d}:{start_raw[1]}-{end_h:02d}:{end_raw[1]}] "

        if start_h > end_h:
            end_h += 24

        start = timedelta(hours=start_h, minutes=start_m)
        end = timedelta(hours=end_h, minutes=end_m)
        duration = end - start

        day_total_hours += duration

    return day_total_hours, blocks_str, msg


def delta_to_time(delta: timedelta) -> str:

    total_seconds = int(delta.total_seconds())

    if total_seconds >= 0:
        hours = total_seconds // 3600
        minutes = (total_seconds // 60) % 60
        prefix = ""
    else:
        total_seconds = -1 * total_seconds
        hours = total_seconds // 3600
        minutes = (total_seconds // 60) % 60
        prefix = "-"

    return f"{prefix}{hours:02d}:{minutes:02d}"


@dataclass
class InternalDay:
    date: datetime.date
    day_total_str: str
    day_total_hours: timedelta
    blocks_str: str
    msg: str
    week_number: int
    week_day_number: int
    week_day_name: str
    month_number: int
    month_name: str
    month_day_number: int
    year_number: int


@dataclass
class State:
    contract_begin = datetime.date(day=1, month=1, year=1970)

    contract_hours_per_week = timedelta(hours=0, minutes=0)
    contract_hours_per_workday = timedelta(
        hours=0, minutes=0
    )  # workday = Mon,Tue,Wed,Thu,Fri

    vacation_days_per_year = 0
    vacation_days_left = 0

    week_target_hours = timedelta(hours=0, minutes=0)
    week_total_hours = timedelta(hours=0, minutes=0)
    week_over_hours = timedelta(hours=0, minutes=0)

    month_total_hours = timedelta(hours=0, minutes=0)
    month_over_hours = timedelta(hours=0, minutes=0)

    year_total_hours = timedelta(hours=0, minutes=0)
    year_over_hours = timedelta(hours=0, minutes=0)

    contract_total_hours = timedelta(hours=0, minutes=0)
    contract_over_hours = timedelta(hours=0, minutes=0)

    all_counted_dates: List[datetime.date] = dc_field(default_factory=list)


def print_contract_result(entry: EmploymentContract) -> None:
    week_target_str = delta_to_time(entry.hours_per_week)
    a = f"{C.RED_TYPE}Contract{C.RS}"
    h = f"{C.GREY}Hours/Week:{C.TIME}{week_target_str}{C.RS}"
    v = f"{C.GREY}VacationDays:{C.TIME}{entry.vacation_days_per_year}{C.RS}"
    print(f"{a} {h} {v}")


def print_balance_result(entry: Balance) -> None:
    a = f"{C.RED_TYPE}Balance {C.GREY}"
    s = ""
    if entry.raise_week_target_by_days:
        s += f"raiseWeekTargetByDays:{C.TIME}{entry.raise_week_target_by_days}"
    if entry.reduce_week_target_by_days:
        s += f"reduceWeekTargetByDays:{C.TIME}{entry.reduce_week_target_by_days}"
    if entry.raise_week_target_by_hours:
        s += f"raiseWeekTargetByHours:{C.TIME}{entry.raise_week_target_by_hours}"
    if entry.reduce_week_target_by_hours:
        s += f"reduceWeekTargetByHours:{C.TIME}{entry.reduce_week_target_by_hours}"
    if entry.add_vacation_days:
        s += f"addVacationDays:{C.TIME}{entry.add_vacation_days}"
    if entry.remove_vacation_days:
        s += f"removeVacationDays:{C.TIME}{entry.remove_vacation_days}"
    print(f"{a} {s}{C.RS} {entry.note}")


def print_day_result(day: InternalDay, entry: Day) -> None:
    if isinstance(entry, HoliDay):
        a = f"{C.HOLIDAY}HoliDay {C.RS}"
    elif isinstance(entry, VacationDay):
        a = f"{C.VACADAY}VacaDay {C.RS}"
    elif isinstance(entry, SickDay):
        a = f"{C.SICKDAY}SickDay {C.RS}"
    elif isinstance(entry, Day):
        a = f"{C.GREY}Day     {C.RS}"

    col = C.WEEKNUM_LI if (day.week_number % 2 == 0) else C.WEEKNUM_DA
    w = f"{col}W{day.week_number:02d}{C.RS}"
    m = f"{col}{day.month_name[0:3]}{C.RS}"
    t = f"{C.TIME}{day.day_total_str}{C.RS}"
    d = f"{C.DATE}{day.date}{C.RS}"
    n = f"{C.GREY}{day.week_day_name[0:3]}{C.RS}"
    b = f"{C.BLOCK}{day.blocks_str}{C.RS}"
    s = day.msg
    print(f"{a} {w} {m} {d} {n} {t} {b} {s}")


def print_week_result(day: InternalDay, state: State) -> None:
    a = f"{C.GREY}Week    {C.RS}"
    col = C.WEEKNUM_LI if (day.week_number % 2 == 0) else C.WEEKNUM_DA
    w = f"{col}W{day.week_number:02d}{C.RS}"
    m = f"{col}{day.month_name[0:3]}{C.RS}"
    t = f"{C.GREY}Total: {C.TIME}{delta_to_time(state.week_total_hours)}{C.RS}"
    o = f"{C.GREY}Over: {C.OVER}{delta_to_time(state.week_over_hours)}{C.RS}"
    print(f"{a} {w} {m} {t}{C.GREY} {o}")


def print_month_result(day: InternalDay, state: State) -> None:
    a = f"{C.GREY}Month   {C.RS}"
    m = f"{C.MONTH_NUM}M{day.month_number:02d}{C.RS}"
    n = f"{C.MONTH_NUM}{day.month_name[0:3]}{C.RS}"
    t = f"{C.GREY}Total: {C.TIME}{delta_to_time(state.month_total_hours)}{C.RS}"
    o = f"{C.GREY}Over: {C.OVER}{delta_to_time(state.month_over_hours)}{C.RS}"
    print(f"{a} {m} {n} {t} {o}")


def print_last_week_result(last_day: InternalDay, state: State) -> None:
    n = (
        f"\n{C.ITALIC}{C.GREY_DA}Note: \n"
        + f"* Over hours for the 'Current Week' are not included in other stats.\n"
        + f"* Holidays, VacationDays, SickDays, etc. reduce the week target hours.{C.RS}\n"
    )
    a = f"\n= After Week {last_day.week_number - 1} = \n"
    r = [
        f"{C.GREY}Vacation Left : {C.TIME}{state.vacation_days_left} d",
        f"{C.GREY}Contract Total: {C.TIME}{delta_to_time(state.contract_total_hours)} h",
        f"{C.GREY}Contract Over : {C.OVER}{delta_to_time(state.contract_over_hours)} h",
        f"{C.GREY}Year Total    : {C.TIME}{delta_to_time(state.year_total_hours)} h",
        f"{C.GREY}Year Over     : {C.OVER}{delta_to_time(state.year_over_hours)} h",
        f"{C.GREY}Month Total   : {C.TIME}{delta_to_time(state.month_total_hours)} h",
        f"{C.GREY}Month Over    : {C.OVER}{delta_to_time(state.month_over_hours)} h",
    ]
    rr = "\n".join(r)
    print(f"{n}{a}{rr}")


def print_current_week_result(last_day: InternalDay, state) -> None:
    a = f"\n{C.RS}= Current Week {last_day.week_number} =\n"
    b = f"{C.GREY}This Week Total: {C.TIME}{delta_to_time(state.week_total_hours)} h\n"
    c = f"{C.GREY}This Week Over : {C.OVER}{delta_to_time(state.week_over_hours)} h"
    print(f"{a}{b}{c}")


def print_date_exists_error(date: datetime.date) -> None:
    m = f"{C.ERROR}ERROR: Same date used multiple times: {date}{C.RS}"
    print(m)
    sys.exit(1)


def process(entries: List[Entry]) -> None:

    state = State()

    # Loop Cache
    last_day: Optional[InternalDay] = None

    for i, entry in enumerate(entries):

        if isinstance(entry, EmploymentContract):

            # We need to reset the hours which have been worked with this contract.
            state.contract_total_hours = timedelta(hours=0, minutes=0)

            state.contract_begin = get_date_from_str(entry.begin)
            state.contract_hours_per_week = entry.hours_per_week
            state.contract_hours_per_workday = entry.hours_per_workday
            state.vacation_days_left = entry.vacation_days_per_year

            state.week_target_hours = entry.hours_per_week

            print_contract_result(entry)

            continue

        if isinstance(entry, Balance):

            state.vacation_days_left += entry.add_vacation_days
            state.vacation_days_left -= entry.remove_vacation_days

            # For Adding/Removing days/hours we raise or lower the week_target_hours, thus
            # producing/removing überstunden

            state.week_target_hours = state.week_target_hours - timedelta(
                hours=entry.reduce_week_target_by_hours
            )
            state.week_target_hours = state.week_target_hours + timedelta(
                hours=entry.raise_week_target_by_hours
            )

            state.week_target_hours = state.week_target_hours - (
                state.contract_hours_per_workday * entry.reduce_week_target_by_days
            )

            state.week_target_hours = state.week_target_hours + (
                state.contract_hours_per_workday * entry.raise_week_target_by_days
            )

            print_balance_result(entry)

            continue

        if isinstance(entry, Day):

            blocks_str = ""
            date = get_date_from_str(entry.date_str)
            day_total_hours, blocks_str, msg = get_day_data(entry.values)

            cur_day = InternalDay(
                date=date,
                day_total_str=delta_to_time(day_total_hours),
                day_total_hours=day_total_hours,
                blocks_str=blocks_str,
                msg=msg,
                week_number=date.isocalendar()[1],
                week_day_number=date.weekday(),
                week_day_name=date.strftime("%A"),
                month_number=date.month,
                month_name=date.strftime("%B"),
                month_day_number=date.day,
                year_number=date.year,
            )

            # Check if date exists
            if cur_day.date in state.all_counted_dates:
                print_date_exists_error(cur_day.date)
            else:
                state.all_counted_dates.append(cur_day.date)

            # On current day is new week
            if last_day and cur_day.week_number != last_day.week_number:

                # We increase the "over" counters after each completed week.
                state.month_over_hours = state.month_over_hours + state.week_over_hours
                state.year_over_hours = state.year_over_hours + state.week_over_hours
                state.contract_over_hours = (
                    state.contract_over_hours + state.week_over_hours
                )

                # Print Log for last week
                print_week_result(last_day, state)

                # Reset reset week counters
                state.week_total_hours = timedelta(hours=0, minutes=0)
                state.week_over_hours = timedelta(hours=0, minutes=0)
                state.week_target_hours = state.contract_hours_per_week

            # On current day is new month
            if last_day and cur_day.month_number != last_day.month_number:

                # Print Log for last month
                print_month_result(last_day, state)

                # Reset month counters
                state.month_total_hours = timedelta(hours=0, minutes=0)
                state.month_over_hours = timedelta(hours=0, minutes=0)

            # On current day is new year
            if last_day and cur_day.year_number != last_day.year_number:

                # TODO: Log year and reset year counters

                # Print Log for last year
                # print_year_result(last_day, state)

                # Reset year counters
                state.year_total_hours = timedelta(hours=0, minutes=0)
                state.year_over_hours = timedelta(hours=0, minutes=0)

            if isinstance(entry, (HoliDay, VacationDay, SickDay)):
                state.week_target_hours = (
                    state.week_target_hours - state.contract_hours_per_workday
                )

            if isinstance(entry, VacationDay):
                state.vacation_days_left = state.vacation_days_left - 1

            print_day_result(cur_day, entry)

            state.week_total_hours = state.week_total_hours + cur_day.day_total_hours
            state.month_total_hours = state.month_total_hours + cur_day.day_total_hours
            state.year_total_hours = state.year_total_hours + cur_day.day_total_hours
            state.contract_total_hours = (
                state.contract_total_hours + cur_day.day_total_hours
            )
            state.week_over_hours = state.week_total_hours - state.week_target_hours

            last_day = cur_day

    if isinstance(last_day, InternalDay):
        print_last_week_result(last_day, state)
        print_current_week_result(last_day, state)
