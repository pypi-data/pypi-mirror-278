from datetime import datetime, timedelta
from enum import Enum

from dateutil.relativedelta import relativedelta


class Periodicity(Enum):
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
    MONTHLY = "MONTHLY"
    YEARLY = "YEARLY"

    def get_next_date(self, current_date: datetime) -> datetime:
        if self == Periodicity.DAILY:
            return current_date + timedelta(days=1)
        elif self == Periodicity.WEEKLY:
            return current_date + timedelta(weeks=1)
        elif self == Periodicity.MONTHLY:
            return (current_date + relativedelta(months=+1)).replace(day=1)
        elif self == Periodicity.YEARLY:
            return (
                current_date +
                relativedelta(
                    years=+
                    1)).replace(
                day=1,
                month=1)
        else:
            raise ValueError(f"Unsupported periodicity: {self.value}")
