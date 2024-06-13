from datetime import datetime, timezone
from functools import partial
from typing import Dict, List, NamedTuple, Optional

from ...domain.model.completion_log import CompletionLog
from ...domain.model.periodicity import Periodicity


class StreakData(NamedTuple):
    """
    Information about a streaks.

    Attributes:
        current_streak (int): Current streak length.
        max_streak (int): Maximum streak length.
        broken_streaks (int): Number of broken streaks.
        consecutive_streaks (Dict[datetime, int]): Consecutive streaks.
    """
    current_streak: int
    max_streak: int
    broken_streaks: int
    consecutive_streaks: Dict[datetime, int]


class Monad:
    """
    A simple implementation of a monad.

    Attributes:
        value: The value contained within the monad.
    """

    def __init__(self, value):
        self.value = value

    def bind(self, func):
        """Applies a function to the value within the monad."""
        return Monad(func(self.value))


def is_log_within_period(
        log_date: datetime,
        period_start: datetime,
        period_end: datetime) -> bool:
    """
    Checks if a log date is within a specified period.

    Args:
        log_date (datetime): The log date.
        period_start (datetime): The start date of the period.
        period_end (datetime): The end date of the period.

    Returns:
        bool: True if log_date is within the period, False otherwise.
    """
    return period_start < log_date <= period_end


def update_streak_data(
        log_date: datetime,
        period_start: datetime,
        period_end: datetime,
        today: datetime,
        streak_data: StreakData) -> StreakData:
    """
    Updates streak data based on a log date.

    Args:
        log_date (datetime): The log date.
        period_start (datetime): The start date of the streak period.
        period_end (datetime): The end date of the streak period.
        today (datetime): The current date.
        streak_data (StreakData): The current streak data.

    Returns:
        StreakData: Updated streak data.
    """
    current_streak, max_streak, broken_streaks, consecutive_streaks = streak_data
    if is_log_within_period(log_date, period_start, period_end):
        current_streak += 1
        consecutive_streaks = {**consecutive_streaks, log_date: current_streak}
    elif period_end <= today and current_streak > 0:
        broken_streaks += 1
        current_streak = 0
        consecutive_streaks = {
            **consecutive_streaks, period_end: current_streak}

    max_streak = max(current_streak, max_streak)
    return StreakData(
        current_streak,
        max_streak,
        broken_streaks,
        consecutive_streaks)


def calculate_streak(
        log_dates: List[CompletionLog],
        period_start: datetime,
        period_end: datetime,
        streak_data: StreakData,
        today: datetime) -> Monad:
    """
    Calculates the streak data for a given period.

    Args:
        log_dates (List[CompletionLog]): List of completion logs.
        period_start (datetime): The start date of the period.
        period_end (datetime): The end date of the period.
        streak_data (StreakData): The current streak data.
        today (datetime): The current date.

    Returns:
        Monad: Monad containing the updated streak data.
    """
    process_log_for_streak = partial(
        update_streak_data,
        period_start=period_start,
        period_end=period_end,
        today=today,
        streak_data=streak_data)
    streaks = (process_log_for_streak(log_date) for log_date in log_dates)
    max_streak_data = max(
        streaks, key=lambda streak: streak.current_streak, default=streak_data)
    return Monad(max_streak_data)


def update_streaks_data_monad(
        current_date: datetime,
        streak_data_monad: Monad,
        log_dates: List[CompletionLog],
        periodicity: Periodicity,
        today: datetime) -> Monad:
    """
    Recursively updates streak data for a sequence of periods.

    Args:
        current_date (datetime): The current date in the sequence.
        streak_data_monad (Monad): Monad containing the current streak data.
        log_dates (List[CompletionLog]): List of completion logs.
        periodicity: The periodicity.
        today (datetime): The current date.

    Returns:
        Monad: Monad containing the updated streak data.
    """
    if current_date > today:
        return streak_data_monad

    next_date = periodicity.get_next_date(current_date)
    updated_streak_data_monad = calculate_streak(
        log_dates, current_date, next_date, streak_data_monad.value, today)

    return update_streaks_data_monad(
        next_date,
        updated_streak_data_monad,
        log_dates,
        periodicity,
        today)


def get_streaks_info(
        logs: List[CompletionLog],
        periodicity: Periodicity,
        creation_date: datetime,
        today: Optional[datetime] = None) -> StreakData:
    """
    Computes the streak data for a given set of logs.

    Args:
        logs (List[CompletionLog]): List of completion logs.
        periodicity: The periodicity.
        creation_date (datetime): The date when the streak tracking started.
        today (Optional[datetime]): The current date.

    Returns:
        StreakData: The computed streak data.
    """
    if not logs:
        return StreakData(0, 0, 0, {})

    today = today or datetime.now(timezone.utc).replace(tzinfo=None)
    log_dates = sorted(log.date for log in logs)

    streaks_data_monad = update_streaks_data_monad(creation_date, Monad(
        StreakData(0, 0, 0, {})), log_dates, periodicity, today)

    return streaks_data_monad.value
