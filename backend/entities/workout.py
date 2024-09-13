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

    # Name of the workout
    name: Mapped[str] = mapped_column(String, nullable=False)

    # Distance of the workout in miles
    distance: Mapped[float] = mapped_column(Float, nullable=False)

    # Duration of the workout in minutes
    duration: Mapped[int] = mapped_column(Integer, nullable=False)

    # The day in which the workout was created
    date: Mapped[str] = mapped_column(String, nullable=False, default=datetime.datetime.now(tz).strftime("%Y-%m-%d"))
    # created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, default=datetime.datetime.now(tz))

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
            date=self.date
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
            date=workout.date
        )