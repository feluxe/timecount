# timecount

## Install

git clone the repo.

pip install --user -e /path/to/repo

## Usage

After installation simply import timecount and start logging:

```python
from timecount import process
from timecount.tctypes import *

# fmt: off
entries = [
    EmploymentContract(begin="01-04-2020", hours_per_week=30, vacation_days_per_year=29),
    Balance(remove_vacation_days=7, note="Contract starts with April, thus remove 3 Month."),
    Balance(reduce_week_target_by_days=2, note="You need to balance for two work days here, because you start in the middle of the week."),

    Day("01-04-2020", [12.30, 20.00], [20.30, 01.15], "Configure Workstation"),
    # ...
]

process(entries)
```
