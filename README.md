# timecount

## Install

Install `timecount` python package via pip from the github repo:

```
pip install --user git+https://github.com/feluxe/timecount.git@master
```

## Usage

Simply create a `timelog.py` file somewhere, import `timecount` and start logging, e.g:

```python
from timecount import process
from timecount.tctypes import *

# fmt: off
entries = [
    EmploymentContract(begin="01-04-2020", hours_per_week=30, vacation_days_per_year=29),
    Balance(remove_vacation_days=7, note="Contract starts with April, thus remove 3 Month."),
    Balance(reduce_week_target_by_days=2, note="You need to balance for two work days here, because you start in the middle of the week."),

    Day("01-04-2020", [12.30, 20.00], [20.30, 01.15], "Configure Workstation"),
    Day("02-04-2020", [12.00, 15.00], "Configure Workstation"),
    Day("03-04-2020", [06.00, 10.00], "Configure Workstation"),
    # ...
]

process(entries)
```

Run `timelog.py` to view the results:

```bash
python timelog.py
```

You might want to create an executable script `~/bin/timelog` with the following content in order to conveniently print logging results in your terminal:

```bash
#!/usr/bin/env bash
python /path/to/timelog.py
```

You can now run `timelog` anywhere from your terminal.

## Example

Look in `./tests` for a more complete example.

