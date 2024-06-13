from pydantic import BaseModel

from ..domain.model.periodicity import Periodicity


class HabitCreateSchema(BaseModel):
    description: str
    periodicity: Periodicity
