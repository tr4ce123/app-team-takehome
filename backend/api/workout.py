from fastapi import APIRouter, Depends

from ..services.workout import WorkoutService
from ..models.workout import Workout

api = APIRouter(prefix="/workouts", tags=["Workouts"])
openapi_tags = {
    "name": "Workouts",
    "description": "Create, update, delete, and retrieve Workouts.",
}

@api.get("/", response_model=list[Workout], tags=["Workouts"])
def get_workouts(workout_service: WorkoutService = Depends(WorkoutService)) -> list[Workout]:
    """
    Get all workouts

    Params:
        workout_service: Service for interacting with workouts

    Returns:
        list[Workout]: All Workouts in the Workouts database table
    """
        
    return workout_service.all()

@api.get("/{workout_id}", response_model=Workout, tags=["Workouts"])
def get_workout_by_id(workout_id: int, workout_service: WorkoutService = Depends(WorkoutService)) -> Workout:
    """
    Get a workout by its ID

    Params:
        workout_id: The ID of the workout to retrieve
        workout_service: Service for interacting with workouts

    Returns:
        Workout: The workout with the specified ID
    """

    return workout_service.get_workout_by_id(workout_id)


@api.post("/", response_model=Workout, tags=["Workouts"])
def create_workout(workout: Workout, workout_service: WorkoutService = Depends(WorkoutService)) -> Workout:
    """
    Create a new workout
    
    Params:
        workout: The workout to create
        workout_service: Service for interacting with workouts
    
    Returns:
        Workout: The newly created workout
    """

    return workout_service.create_workout(workout)


@api.put("/{workout_id}", response_model=Workout, tags=["Workouts"])
def update_workout(workout: Workout, workout_service: WorkoutService = Depends(WorkoutService)) -> Workout:
    """
    Update a workout

    Params:
        workout: The updated workout
        workout_service: Service for interacting with workouts
    
    Returns:
        Workout: The updated workout
    """

    return workout_service.update_workout(workout)


@api.delete("/{workout_id}", response_model=None, tags=["Workouts"])
def delete_workout(workout_id: int, workout_service: WorkoutService = Depends(WorkoutService)) -> None:
    """
    Delete a workout based on its ID

    Params:
        workout_id: The ID of the workout to delete
        workout_service: Service for interacting with workouts
    
    Returns:
        None
    """

    workout_service.delete_workout(workout_id)