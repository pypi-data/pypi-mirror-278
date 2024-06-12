from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship

from ...domain.model.periodicity import Periodicity

Base = declarative_base()


class HabitModel(Base):
    __tablename__ = 'habits'

    id = Column(Integer, primary_key=True)
    description = Column(String)
    periodicity = Column(Enum(Periodicity))
    creation_date = Column(DateTime, default=datetime.now(timezone.utc))
    completion_logs = relationship(
        "CompletionLogModel", back_populates="habit")


class CompletionLogModel(Base):
    __tablename__ = 'completion_logs'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=datetime.now(timezone.utc))
    habit_id = Column(Integer, ForeignKey('habits.id'))
    habit = relationship("HabitModel", back_populates="completion_logs")
