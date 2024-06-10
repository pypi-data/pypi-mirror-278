import schedule as py_schedule
from typing import Optional, Tuple, Callable
import datetime


class Period:
    def __init__(
        self,
        years: int = 0,
        months: int = 0,
        weeks: int = 0,
        days: int = 0,
        hours: int = 0,
        minutes: int = 0,
        seconds: int = 0,
        at: Optional[str] = None,
        tz: Optional[str] = None,
    ) -> None:
        """
        Class to represent a period of time.
        :param years: The number of years to wait. Default is 0.
        :param months: The number of months to wait. Default is 0.
        :param weeks: The number of weeks to wait. Default is 0.
        :param days: The number of days to wait. Default is 0.
        :param hours: The number of hours to wait. Default is 0.
        :param minutes: The number of minutes to wait. Default is 0.
        :param seconds: The number of seconds to wait. Default is 0.
        :param at: The time to run the job at. Format: HH:MM. Default is None.
        :param tz: The timezone to run the job in. Format: Continent/City. Default is None.
        """
        self.years = years
        self.months = months
        self.weeks = weeks
        self.days = days
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds
        self.at = at
        self.tz = tz

    def get_interval(self) -> py_schedule.Job:
        period = py_schedule.every(
            self.seconds + self.minutes * 60 + self.hours * 3600 + self.days * 86400
        ).seconds

        return period.at(self.at, self.tz) if self.at else period

    def run(self, job, *args, **kwargs):
        return self.get_interval().do(job, *args, **kwargs)

    def __str__(self) -> str:
        return (
            f"every {self.years} years, " * bool(self.years)
            + f"{self.months} months, " * bool(self.months)
            + f"{self.weeks} weeks, " * bool(self.weeks)
            + f"{self.days} days, " * bool(self.days)
            + f"{self.hours} hours, " * bool(self.hours)
            + f"{self.minutes} minutes, " * bool(self.minutes)
            + f"{self.seconds} seconds" * bool(self.seconds)
            + (f" at {self.at} in {self.tz}" if self.at else "")
        ).rstrip(", ")


ScriptList = list[Tuple[Optional[datetime.datetime], Optional[Period], Callable, str]]
scripts_to_run_now: ScriptList = []  # Stores the scripts to schedule immediately
scripts_to_run_later: ScriptList = (
    []
)  # Stores the scripts to schedule later in the following format: (start_datetime, script_func)


def script_factory(
    script: Callable,
    repeats: Optional[Period],
    *args,
    **kwargs,
) -> Callable:
    """
    Factory function to create a new periodic job.
    """
    if not repeats:

        def script_func():
            return script(*args, **kwargs)

        return script_func

    def repeated_script_func():
        return repeats.run(script, *args, **kwargs)

    return repeated_script_func


def schedule(
    for_time: Optional[datetime.datetime] = None,
    repeats: Optional[Period] = None,
    *args,
    **kwargs,
):
    """
    Decorator to schedule a new periodic job.

    :param for_time: The date to start the job. If None, the job will start immediately.
    :param repeats: The period of the job. If None, the job will run only once.
    :param args: The arguments to pass to the decorated function.
    :param kwargs: The keyword arguments to pass to the decorated function.
    """

    def schedule_decorator(func):
        script_func = script_factory(func, repeats, *args, **kwargs)
        if not for_time:
            scripts_to_run_now.append((for_time, repeats, script_func, func.__name__))
        else:
            scripts_to_run_later.append((for_time, repeats, script_func, func.__name__))

    return schedule_decorator
