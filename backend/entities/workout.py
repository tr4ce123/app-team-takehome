"""Definition of a SQLAlchemy table-backed object mapping entity for workouts."""

import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean

from ..models.workout import Workout
from ..database import Base

from sqlalchemy.orm import  Mapped, mapped_column
from pytz import timezone
tz = timezone("EST")

class WorkoutEntity(Base):
    """SQLAlchemy entity representing a workout."""

    __tablename__ = "workout"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    distance: Mapped[float] = mapped_column(Float, nullable=False)
    duration: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, default=datetime.datetime.now(tz))

    def to_model(self) -> Workout:
        """
        Converts a Workout Entity object into a Workout Pydantic Model object

        Returns:
            Workout: A Workout Pydantic Model object
        """

        return Workout(
            id=self.id,
            name=self.name,
            distance=self.distance,
            duration=self.duration,
            created_at=self.created_at
        )
    
    @classmethod
    def from_model(cls, workout: Workout) -> "WorkoutEntity":
        """
        Class method that converts a Workout Pydantic Model object into a Workout Entity object

        Params:
            workout (Workout): A Workout Pydantic Model object

        Returns:
            WorkoutEntity: Entity created from model
        """

        return cls(
            id=workout.id,
            name=workout.name,
            distance=workout.distance,
            duration=workout.duration,
            created_at=workout.created_at
        )