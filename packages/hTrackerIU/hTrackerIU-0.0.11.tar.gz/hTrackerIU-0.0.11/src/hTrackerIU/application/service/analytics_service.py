from datetime import datetime
from typing import List

from ...domain.model.completion_log import CompletionLog
from ...domain.model.periodicity import Periodicity
from ...domain.service.streak_calculation_service import get_streaks_info
from ...infrastructure.repository.habit_repository import HabitRepository


class AnalyticsService:
    def __init__(self, repository: HabitRepository):
        self.repository = repository

    @staticmethod
    def current_streak(
            logs: List[CompletionLog],
            periodicity: str,
            creation_date: datetime,
            today: datetime = None) -> int:
        return get_streaks_info(
            logs,
            periodicity,
            creation_date,
            today).current_streak

    @staticmethod
    def longest_streak(
            logs: List[CompletionLog],
            periodicity: str,
            creation_date: datetime,
            today: datetime = None) -> int:
        return get_streaks_info(
            logs, periodicity, creation_date, today).max_streak

    @staticmethod
    def broken_streaks_count(
            logs: List[CompletionLog],
            periodicity: str,
            creation_date: datetime,
            today: datetime = None) -> int:
        return get_streaks_info(
            logs,
            periodicity,
            creation_date,
            today).broken_streaks

    @staticmethod
    def consecutive_streaks(
            logs: List[CompletionLog],
            periodicity: str,
            creation_date: datetime,
            today: datetime = None) -> int:
        return get_streaks_info(
            logs,
            periodicity,
            creation_date,
            today).consecutive_streaks

    @staticmethod
    def is_current_period_marked(
            logs: List[CompletionLog],
            periodicity: Periodicity,
            today: datetime) -> bool:
        if not logs:
            return False

        latest_log = max(logs, key=lambda log: log.date)
        start_of_next_period = periodicity.get_next_date(latest_log.date)

        return today < start_of_next_period

    def list_habits_by_periodicity(self, periodicity: Periodicity) -> list:
        return self.repository.find_by_periodicity(periodicity)

    def longest_streak_for_all_habits(self) -> int:
        habits = self.repository.get_all()
        max_streaks = [
            self.longest_streak(
                habit.completion_logs,
                habit.periodicity,
                habit.creation_date) for habit in habits]
        return max(max_streaks, default=0)

    def longest_streak_for_habit(self, habit_id: int) -> int:
        habit = self.repository.find_by_id(habit_id)
        return self.longest_streak(
            habit.completion_logs,
            habit.periodicity,
            habit.creation_date) if habit else 0

    def struggled_habits_last_month(self, today: datetime = None) -> list:

        habits = self.repository.get_all()
        struggled_habits = []

        for habit in habits:
            count = self.broken_streaks_count(
                habit.completion_logs,
                habit.periodicity,
                habit.creation_date,
                today)
            if count > 3:
                struggled_habits.append({"habit": {
                    "id": habit.id,
                    "description": habit.description,
                }})

        return struggled_habits
