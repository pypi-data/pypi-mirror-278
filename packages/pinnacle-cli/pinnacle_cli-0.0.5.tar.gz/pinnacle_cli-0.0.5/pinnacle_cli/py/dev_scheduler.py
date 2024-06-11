import schedule
from typing import Optional
from datetime import datetime
import time
from pinnacle_python.schedules import scripts_to_run_now, scripts_to_run_later, Period
from pinnacle_cli.py.import_modules import import_modules

import_modules()


def print_scheduled_script(
    func_name: str, for_time: Optional[datetime], repeats: Optional[Period]
) -> None:
    print(
        f"Scheduled {func_name} to run "
        + (f"at {for_time}" if for_time else "now")
        + (f" that repeats {repeats}" if repeats else " only once")
    )


def run_scheduled(delay: int = 1):
    scripts_to_run_later.sort(key=lambda x: x[0] if x[0] is not None else datetime.min)
    for for_time, repeats, script, func_name in scripts_to_run_now:
        print_scheduled_script(func_name, for_time, repeats)
        script()
    for for_time, repeats, _, func_name in scripts_to_run_later:
        print_scheduled_script(func_name, for_time, repeats)

    while True:
        if (
            scripts_to_run_later
            and scripts_to_run_later[0][0] is not None
            and scripts_to_run_later[0][0] <= datetime.now()
        ):
            scripts_to_run_later[0][2]()
            scripts_to_run_later.pop(0)

        schedule.run_pending()

        time.sleep(delay)
