from datetime import datetime, timedelta
from pytz import timezone

from backend.models.weather import Weather
tz = timezone("EST")

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
    

    def get_weekly_workouts(self) -> list[Workout]:
        """
        Retrieves all workouts from the past 7 days.

        Returns:
            list[Workout]: All Workouts from the current week
        """

        start_date = datetime.now(tz).date()
        end_date = start_date - timedelta(days=7)

        query = select(WorkoutEntity).filter(WorkoutEntity.date <= start_date, WorkoutEntity.date >= end_date)
        entities = self._session.scalars(query).all()

        return [entity.to_model() for entity in entities]
    

    def get_total_weekly_aggreate_workout_data(self, data_point: str) -> float:
        """
        Retrieves the aggregate of a specific workout data point from the last 7 days.
        
        Params:
            data_point: The data point to aggregate
            
        Returns:
            float: The aggregate of the specified data point
        """

        start_date = datetime.now(tz).date()
        end_date = start_date - timedelta(days=7)

        query = select(WorkoutEntity).filter(WorkoutEntity.date <= start_date, WorkoutEntity.date >= end_date)
        entities = self._session.scalars(query).all()

        if data_point == "distance":
            return sum([entity.distance for entity in entities])
        elif data_point == "duration":
            return sum([entity.duration for entity in entities])
        else:
            raise HTTPException(status_code=400, detail="Invalid data point. Enter 'distance' or 'duration'")
        

    def get_average_weekly_aggreate_workout_data(self, data_point: str) -> float:
        """
        Retrieves the average of a specific workout data point from the last 7 days.
        
        Params:
            data_point: The data point to aggregate
            
        Returns:
            float: The average of the specified data point
        """

        start_date = datetime.now(tz).date()
        end_date = start_date - timedelta(days=7)

        query = select(WorkoutEntity).filter(WorkoutEntity.date <= start_date, WorkoutEntity.date >= end_date)
        entities = self._session.scalars(query).all()

        if data_point == "distance":
            return round(sum([entity.distance for entity in entities]) / len(entities), 2)
        elif data_point == "duration":
            return round(sum([entity.duration for entity in entities]) / len(entities), 2)
        else:
            raise HTTPException(status_code=400, detail="Invalid data point. Enter 'distance' or 'duration'")
        

    def get_personal_best_distance(self) -> str:
        """
        Retrieves the personal bests for distance and duration
        
        Returns:
            str: The personal bests for distance and duration
        """

        query = select(WorkoutEntity).order_by(WorkoutEntity.distance.desc())
        distance_entity = self._session.scalars(query).first()

        return f"Personal best distance: {distance_entity.distance} miles!"
    

    def get_personal_best_duration_per_mile(self) -> str:
        """
        Retrieves the personal bests for distance and duration
        
        Returns:
            str: The personal bests for distance and duration
        """

        query = select(WorkoutEntity)
        entities = self._session.scalars(query).all()

        minimum = min([entity.duration / entity.distance for entity in entities])

        return f"Your personal best time per mile is {minimum} minutes per mile!"
    

    def create_workout(self, workout: Workout, weather: Weather) -> Workout:
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
        
        if weather is not None:
            entity.weather_id = weather.id

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

        if entity is None:
            raise HTTPException(status_code=404, detail=f"No workout with ID: { workout.id } to update")

        entity.name = workout.name
        entity.distance = workout.distance
        entity.duration = workout.duration
        entity.date = workout.date

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