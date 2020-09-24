# timecount

Work time tracking for hackers.

## Requirements

Python `>= 3.8`

## Install

Install the `timecount` python package via pip from pypi.org:

```
pip install --user timecount
```

## Getting Started

Simply create an executable file `~/timelog` (it doesn't matter where you put it) with the following example content:

```python
#!/usr/bin/env python3
from timecount import process
from timecount.tctypes import (
    EmploymentContract,
    Balance,
    Day,
    HoliDay,
    SickDay,
    VacationDay,
)

# fmt: off
entries = [

    EmploymentContract(begin="01-04-2020", hours_per_week=30, vacation_days_per_year=23),
    Balance(remove_vacation_days=7, note="Contract starts with April, thus remove 3 Month."),
    Balance(reduce_week_target_by_days=2, note="You need to balance for two work days here, because you start in the middle of the week."),

    Day("01-04-2020", (12.30, 20.00), (20.30, 01.15), "Configure Workstation"),
    Day("02-04-2020", (14.30, 00.30), "Configure Workstation"),
    Day("03-04-2020", (10.30, 15.00), "Configure Workstation"),
    Day("06-04-2020", (10.00, 14.30), (17.00, 22.15) , "Pair Programming Daniel."),

    Day("07-04-2020", (10.30, 14.30), (15.30, 21.45) , "Pair Programming Daniel."),
    SickDay("08-04-2020", "Covid19")
    Day("09-04-2020", (11.00, 15.00), (19.30, 22.00) , "Meeting; Try test automation."),

    HoliDay("10-04-2020", (12.00, 13.00), "Karfreitag; Tooling"), # I worked on this holiday..
    Day("11-04-2020", (11.00, 14.00), (21.15, 00.00), "Tooling, Testing."),
    Day("12-04-2020", (11.15, 13.15), "Configure Workstation; Tooling;"),

    HoliDay("13-04-2020", (11.00, 16.00), "Ostermontag; Slack Channel Catchup; System Setup; Tooling"),
    Day("14-04-2020", (11.00, 14.00), (15.30, 18.30), "Tooling; SlackMeetings;"),

   # Continue with your logs ...
]

process(entries)
```

Now run `~/timelog` in your terminal to see the results.

For convenience I suggest creating a symlink for the `timelog` file in your `~/bin` directory, so you can call `timelog` from anywhere in your terminal:

```bash
ln -s ~/timelog ~/bin/timelog
```

## Entry Types

For a list of EntryTypes and their arguments, see `tctypes.py`.

## Examples

Look in `./tests` for a more complete example.
