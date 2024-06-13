from fastapi import Depends
from sqlalchemy.orm import Session

from ..application.service.analytics_service import AnalyticsService
from ..application.service.habit_service import HabitService
from ..infrastructure.orm.session import SessionLocal
from ..infrastructure.repository.habit_repository import HabitRepository


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_habit_repository(db: Session = Depends(get_db)):
    return HabitRepository(db)


def get_analytics_service(
        habit_repository: HabitRepository = Depends(get_habit_repository)):
    return AnalyticsService(repository=habit_repository)


def get_habit_service(
        habit_repository: HabitRepository = Depends(get_habit_repository),
        analytics_service: AnalyticsService = Depends(get_analytics_service)):
    return HabitService(
        repository=habit_repository,
        analytics_service=analytics_service)
