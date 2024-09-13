from fastapi import APIRouter, Depends

from backend.services.weather import WeatherService

from ..services.workout import WorkoutService
from ..models.workout import Workout
from ..services.openai import OpenAIService

api = APIRouter(prefix="/workouts", tags=["Workouts"])
openapi_tags = {
    "name": "Workouts",
    "description": "Create, update, delete, and retrieve Workouts. Retrieve aggregate data from the last 7 days.",
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


@api.get("/weekly/workouts", response_model=list[Workout], tags=["Workouts"])
def get_weekly_workouts(workout_service: WorkoutService = Depends(WorkoutService)) -> list[Workout]:
    """
    Get all workouts logged from the last 7 days

    Params:
        workout_service: Service for interacting with workouts

    Returns:
        list[Workout]: All Workouts from the current week
    """

    return workout_service.get_weekly_workouts()


@api.get("/weekly/{data_point}/sum", response_model=float, tags=["Workouts"])
def get_aggregate_workout_data(data_point: str, workout_service: WorkoutService = Depends(WorkoutService)) -> float:
    """
    Get the aggregate of a specific workout data point from the last 7 days

    Params:
        data_point: The data point to aggregate
        workout_service: Service for interacting with workouts

    Returns:
        float: The aggregate of the specified data point
    """

    return workout_service.get_total_weekly_aggreate_workout_data(data_point)


@api.get("/weekly/{data_point}/average", response_model=float, tags=["Workouts"])
def get_average_workout_data(data_point: str, workout_service: WorkoutService = Depends(WorkoutService)) -> float:
    """
    Get the average of a specific workout data point from the last 7 days. The average is represented by the sum of the data point divided by the number of workouts.

    Params:
        data_point: The data point to average
        workout_service: Service for interacting with workouts

    Returns:
        float: The average of the specified data point
    """

    return workout_service.get_average_weekly_aggreate_workout_data(data_point)


@api.get("/personal-bests/distance", response_model=str, tags=["Workouts"])
def get_personal_best_distance(workout_service: WorkoutService = Depends(WorkoutService)) -> str:
    """
    Get the personal best distance and duration 

    Params:
        workout_service: Service for interacting with workouts

    Returns:
        str: The personal best distance
    """

    return workout_service.get_personal_best_distance()


@api.get("/personal-bests/duration", response_model=str, tags=["Workouts"])
def get_personal_best_duration(workout_service: WorkoutService = Depends(WorkoutService)) -> str:
    """
    Get the personal best duration

    Params:
        workout_service: Service for interacting with workouts

    Returns:
        str: The personal best duration
    """

    return workout_service.get_personal_best_duration_per_mile()


@api.get("/advice/weather/outfit/{city}", response_model=str, tags=["Workouts"])
def get_workout_outfit_advice_by_location(city: str, weather_service: WeatherService = Depends(WeatherService), openai_service: OpenAIService = Depends(OpenAIService)) -> str:
    """
    Get an outfit suggestion for a workout based on the weather

    Params:
        weather: The weather data for the location
        workout_service: Service for interacting with workouts

    Returns:
        str: The outfit suggestion
    """

    weather = weather_service.get_current_weather_by_location(city)

    return openai_service.generate_workout_outfit(weather)


@api.get("/advice/improvement/", response_model=str, tags=["Workouts"])
def get_workout_improvement_advice( workout_service: WorkoutService = Depends(WorkoutService), openai_service: OpenAIService = Depends(OpenAIService)) -> str:
    """
    Get advice on how to improve a workout based on weekly averages

    Params:
        workout_id: The ID of the workout to get advice for
        workout_service: Service for interacting with workouts
        openai_service: Service for interacting with the OpenAI API

    Returns:
        str: The improvement advice
    """

    average_distance_per_workout = workout_service.get_average_weekly_aggreate_workout_data("distance")
    average_duration_per_workout = workout_service.get_average_weekly_aggreate_workout_data("duration")

    return openai_service.generate_workout_improvement_advice(average_distance_per_workout, average_duration_per_workout)


@api.post("/", response_model=Workout, tags=["Workouts"])
def create_workout(workout: Workout, weather_service: WeatherService = Depends(WeatherService), workout_service: WorkoutService = Depends(WorkoutService)) -> Workout:
    """
    Create a new workout
    
    Params:
        workout: The workout to create
        workout_service: Service for interacting with workouts
        city: The city to get the weather
        weather_service: Service for interacting with weather data
    
    Returns:
        Workout: The newly created workout
    """

    weather = weather_service.get_current_weather_by_location(workout.city)

    return workout_service.create_workout(workout, weather)


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