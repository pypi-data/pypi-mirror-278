import datetime
import random
from sqlalchemy.orm import sessionmaker

from .domain.model.periodicity import Periodicity
from .infrastructure.orm.models import Base, CompletionLogModel, HabitModel
from .infrastructure.orm.session import engine

Session = sessionmaker(bind=engine)


def generate_dates(start_date, periodicity, count, irregular=False):
    dates = []
    current_date = start_date

    for _ in range(count):
        if irregular and periodicity == Periodicity.DAILY:
            current_date += datetime.timedelta(days=random.randint(1, 2))
        elif periodicity == Periodicity.DAILY:
            current_date += datetime.timedelta(days=1)
        elif periodicity == Periodicity.WEEKLY:
            current_date += datetime.timedelta(weeks=1)
        elif periodicity == Periodicity.MONTHLY:
            current_date += datetime.timedelta(days=30)
        elif periodicity == Periodicity.YEARLY:
            current_date += datetime.timedelta(days=365)
        dates.append(current_date)

    return dates


def init_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    session = Session()

    habits_data = [
        {"description": "60m Running",
         "periodicity": Periodicity.DAILY,
         "start_date": datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=29),
         "logs_count": 30},
        {"description": "10m Meditation",
         "periodicity": Periodicity.DAILY,
         "start_date": datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=29),
         "logs_count": 10,
         "irregular": True},
        {"description": "3h Hiking",
         "periodicity": Periodicity.WEEKLY,
         "start_date": datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(weeks=4),
         "logs_count": 4},
        {"description": "3h Swimming",
         "periodicity": Periodicity.MONTHLY,
         "start_date": datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=30 * 12),
         "logs_count": 12},
        {"description": "20d Traveling",
         "periodicity": Periodicity.YEARLY,
         "start_date": datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=365 * 3),
         "logs_count": 3}
    ]

    for habit_data in habits_data:
        habit = HabitModel(
            description=habit_data["description"],
            periodicity=habit_data["periodicity"],
            creation_date=habit_data["start_date"]
        )
        session.add(habit)
        log_dates = generate_dates(
            habit_data["start_date"],
            habit_data["periodicity"],
            habit_data["logs_count"],
            habit_data.get("irregular", False))

        for date in log_dates:
            log = CompletionLogModel(date=date, habit=habit)
            session.add(log)

    session.commit()
    session.close()

    return "Database initialized with sample data!"


if __name__ == "__main__":
    init_database()
