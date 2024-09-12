from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException

from backend.entities.workout import WorkoutEntity
from backend.models.workout import Workout
from ..database import db_session

class WorkoutService:
    def __init__(self, session: Session = Depends(db_session)):
        self._session = session

    def all(self) -> list[Workout]:
        """
        Retrieves all workouts from the table

        Returns:
            list[Workout]: List of all Workouts
        """

        query = select(WorkoutEntity)
        entities = self._session.scalars(query).all()

        return [entity.to_model() for entity in entities]
    
    def get_workout_by_id(self, workout_id: int) -> Workout:
        """
        Retrieves a workout by its ID.
        Raises an error if no workout with the given ID is found.
        
        Params:
            workout_id: The ID of the workout to retrieve
            
        Returns:
            Workout: The workout with the specified ID
        """
        
        entity = self._session.get(WorkoutEntity, workout_id)

        if entity is None:
            raise HTTPException(status_code=404, detail=f"Workout with ID: { workout_id } does not exist")
        
        return entity.to_model()
    
    def create_workout(self, workout: Workout) -> Workout:
        """
        Creates a new workout. 
        Raises an error if a workout with the same ID already exists.
        
        Params:
            workout: The workout to create
        
        Returns:
            Workout: The newly created workout
        """

        existing_workout = self._session.query(WorkoutEntity).filter(WorkoutEntity.id == workout.id).one_or_none()
        if existing_workout:
            raise HTTPException(status_code=400, detail="Workout with this ID already exists")

        entity = WorkoutEntity.from_model(workout)

        self._session.add(entity)
        self._session.commit()

        return entity.to_model()
    
    def update_workout(self, workout: Workout) -> Workout:
        """
        Updates a workout

        Params:
            workout: The updated workout

        Returns:
            Workout: The newly updated workout
        """

        entity = self._session.get(WorkoutEntity, workout.id)
        entity.name = workout.name
        entity.distance = workout.distance
        entity.duration = workout.duration
        entity.created_at = workout.created_at

        self._session.commit()

        return entity.to_model()
    
    def delete_workout(self, workout_id: int) -> None:
        """
        Deletes a workout by its ID.
        Raises an error if there is no workout with the given ID to delete.

        Params:
            workout_id: The ID of the workout to delete
        
        Returns:
            None
        """

        entity = self._session.get(WorkoutEntity, workout_id)

        if entity is None:
            raise HTTPException(status_code=404, detail=f"No workout with ID: { workout_id } to delete")

        self._session.delete(entity)
        self._session.commit()

    # TODO:
    # Create a few methods that get aggregated data such as distance per week, average duration, etc.
        