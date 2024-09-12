from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import Depends

from backend.entities.workout import WorkoutEntity
from backend.models.workout import Workout
from ..database import db_session

class WorkoutService:
    def __init__(self, session: Session = Depends(db_session)):
        self._session = session

    def all(self) -> list[Workout]:

        query = select(WorkoutEntity)
        entities = self._session.scalars(query).all()

        return [entity.to_model() for entity in entities]
    
    def create_workout(self, workout: Workout) -> Workout:

        entity = WorkoutEntity.from_model(workout)
        self._session.add(entity)
        self._session.commit()

        return entity.to_model()
    
    def update_workout(self, workout: Workout) -> Workout:
        entity = self._session.get(WorkoutEntity, workout.id)
        entity.name = workout.name
        entity.distance = workout.distance
        entity.duration = workout.duration
        entity.created_at = workout.created_at

        self._session.commit()

        return entity.to_model()
    
    def delete_workout(self, workout_id: int) -> None:
        entity = self._session.get(WorkoutEntity, workout_id)
        self._session.delete(entity)
        self._session.commit()

    