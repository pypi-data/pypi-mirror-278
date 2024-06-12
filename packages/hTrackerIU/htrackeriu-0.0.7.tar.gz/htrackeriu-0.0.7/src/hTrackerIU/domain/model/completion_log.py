from datetime import datetime, timezone


class CompletionLog:
    def __init__(self, date: datetime = None):
        self.date = date or datetime.now(timezone.utc)
