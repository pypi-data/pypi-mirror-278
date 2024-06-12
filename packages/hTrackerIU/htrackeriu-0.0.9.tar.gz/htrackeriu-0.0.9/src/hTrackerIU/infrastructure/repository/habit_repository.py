from typing import List, Optional

from sqlalchemy.orm import Session

from ...domain.model.habit import Habit
from ...domain.model.completion_log import CompletionLog
from ...domain.model.periodicity import Periodicity
from ...infrastructure.orm.models import CompletionLogModel, HabitModel


class HabitRepository:
    def __init__(self, session: Session):
        self.session = session

    def _to_domain_entity(self, habit_model: HabitModel) -> Habit:
        habit = Habit(
            id=habit_model.id,
            description=habit_model.description,
            periodicity=Periodicity(habit_model.periodicity),
            creation_date=habit_model.creation_date
        )
        habit.completion_logs = [
            CompletionLog(date=log.date)
            for log in habit_model.completion_logs
        ]
        return habit

    def _to_persistence_model(self, habit: Habit) -> HabitModel:
        habit_model = self.session.get(HabitModel, habit.id)
        habit_model.description = habit.description
        habit_model.periodicity = habit.periodicity.value
        habit_model.creation_date = habit.creation_date
        return habit_model

    def _to_new_persistence_model(self, habit: Habit) -> HabitModel:
        habit_model = HabitModel(
            description=habit.description,
            periodicity=habit.periodicity.value,
            creation_date=habit.creation_date
        )

        return habit_model

    def add(self, habit: Habit) -> Habit:
        habit_model = self._to_new_persistence_model(habit)
        self.session.add(habit_model)
        self.session.commit()
        return self._to_domain_entity(habit_model)

    def save(self, habit: Habit) -> None:
        habit_model = self._to_persistence_model(habit)
        existing_log_dates = {log.date for log in habit_model.completion_logs}
        for log in habit.completion_logs:
            if log.date not in existing_log_dates:
                habit_model.completion_logs.append(
                    CompletionLogModel(habit_id=habit.id, date=log.date)
                )
        self.session.commit()

    def remove(self, habit: Habit):
        db_habit = self.session.get(HabitModel, habit.id)
        if db_habit:
            self.session.delete(db_habit)
            self.session.commit()

    def find_by_id(self, habit_id: int) -> Optional[Habit]:
        habit_model = self.session.get(HabitModel, habit_id)
        return self._to_domain_entity(habit_model) if habit_model else None

    def get_all(self) -> List[Habit]:
        habit_models = self.session.query(HabitModel).all()
        return [self._to_domain_entity(habit_model)
                for habit_model in habit_models]

    def find_by_periodicity(self, periodicity: Periodicity) -> List[Habit]:
        habit_models = self.session.query(HabitModel).filter(
            HabitModel.periodicity == periodicity.value
        ).all()
        return [self._to_domain_entity(habit_model)
                for habit_model in habit_models]
