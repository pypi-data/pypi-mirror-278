from datetime import datetime, timezone

from .completion_log import CompletionLog
from .periodicity import Periodicity


class Habit:
    def __init__(
            self,
            description: str,
            periodicity: Periodicity,
            creation_date: datetime = None,
            id: int = None):
        self.id = id
        self.description = description
        self.periodicity = periodicity
        self.creation_date = creation_date or datetime.now(timezone.utc)
        self.completion_logs = []

    def complete(self):
        completion_log = CompletionLog()
        self.completion_logs.append(completion_log)
